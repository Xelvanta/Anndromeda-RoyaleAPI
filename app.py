"""
app.py

Quart-based API that fetches Traderie item data by calling
a long-lived Puppeteer Node.js service over HTTP.

This design avoids subprocess spawning and enables efficient
concurrent scraping with preserved browser state.
"""

import asyncio
from datetime import datetime, timezone
from functools import wraps
import json
import logging
import os
import platform
import signal
import sys
import aiohttp
import aiosqlite
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import abort, Quart, jsonify, request
from quart_cors import cors

# -------------------- Logging --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- Load config --------------------
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config_data = json.load(f)

PYTHON_CONFIG = config_data.get("python_service", {})
CONCURRENT_PAGES = PYTHON_CONFIG.get("concurrent_pages", 5)
MAX_RETRIES = PYTHON_CONFIG.get("max_retries", 3)
NODE_SERVICE_URL = PYTHON_CONFIG.get("node_service_url", "http://localhost:3001/traderie")

# Add a Semaphore to limit global concurrent scraping tasks
# This should match or be slightly lower than MAX_PAGES in your Node config
scraper_semaphore = asyncio.Semaphore(PYTHON_CONFIG.get("concurrent_pages", 5))

# Port / Bind Resolution
PORT = os.environ.get("PORT")
if PORT:
    # Production
    BIND = f"0.0.0.0:{PORT}"
    logger.info(f"Using 0.0.0.0 with PORT from environment variable: {PORT}")
else:
    # Local development
    BIND = PYTHON_CONFIG.get("bind", "127.0.0.1:5000")
    logger.info(f"Using local bind from config.json: {BIND}")

# -------------------- App Setup --------------------

app = Quart(__name__)
cors(app)

# Use environment variable if set, otherwise fall back to config.json
API_KEY = os.getenv("API_KEY") or PYTHON_CONFIG.get("api_key")

def require_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        # Check X-API-Key header
        auth_header = request.headers.get("X-API-Key")
        if not auth_header or auth_header != API_KEY:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            abort(401) # Unauthorized
        return await f(*args, **kwargs)
    return decorated

# ------------------ Node Service -----------------
NODE_SCRIPT = os.path.join(os.path.dirname(__file__), "fetchData.js")
node_process = None
node_retries = 0
NODE_MAX_RETRIES = MAX_RETRIES

async def start_node_service():
    global node_process, node_retries
    
    # If already running, don't start another
    if node_process and node_process.returncode is None:
        return

    node_command = ["node", NODE_SCRIPT]
    node_process = await asyncio.create_subprocess_exec(
        *node_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    label = "Initial start" if node_retries == 0 else f"Restart attempt {node_retries}"
    logger.info(f"🟢 Node service started with PID: {node_process.pid} ({label})")

    # Read stdout until we see the ready signal
    while True:
        line = await node_process.stdout.readline()
        if not line: break
        decoded = line.decode().strip()
        logger.info(f"[Node stdout] {decoded}")
        if "NODE_READY" in decoded:
            logger.info("✅ Node signaled ready")
            node_retries = 0
            break

def stop_node_service():
    global node_process
    if node_process and node_process.returncode is None:
        logger.info("🛑 Stopping Node.js service...")
        if platform.system() == "Windows":
            node_process.terminate()  # safe on Windows
        else:
            node_process.send_signal(signal.SIGINT)

async def node_watchdog():
    global node_process, node_retries
    while True:
        await asyncio.sleep(2)
        if node_process is not None:
            ret = node_process.returncode
            if ret is not None:
                logger.warning(f"❌ Node process (PID {node_process.pid}) exited with code {ret}")
                
                if node_retries < NODE_MAX_RETRIES:
                    node_retries += 1 
                    logger.info(f"♻️ Restarting Node (failure {node_retries}/{NODE_MAX_RETRIES})")
                    await start_node_service() 
                else:
                    logger.critical(f"❌ Max consecutive retries ({NODE_MAX_RETRIES}) reached. Node service disabled.")
                    node_process = None

# ------------------- Item Indexing (SQLite) -------------------

DB_FILE = os.path.join(os.path.dirname(__file__), "item_index.db")
db_conn = None # Global connection for efficiency

async def init_db():
    global db_conn
    db_conn = await aiosqlite.connect(DB_FILE)
    
    # ENABLE MULTIPLE READERS: WAL mode allows reading while writing
    await db_conn.execute("PRAGMA journal_mode=WAL;")
    # Prevent "Database is locked" errors by waiting up to 5 seconds
    await db_conn.execute("PRAGMA busy_timeout = 5000;")
    
    await db_conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT,
            page INTEGER,
            last_seen TEXT
        )
    """)
    await db_conn.commit()

async def update_index_db(items_with_pages):
    if not items_with_pages: return
    try:
        data = [
            (item.get("id"), item.get("name"), page, datetime.now(timezone.utc).isoformat())
            for item, page in items_with_pages if item.get("id")
        ]
        await db_conn.executemany("""
            INSERT OR REPLACE INTO items (id, name, page, last_seen)
            VALUES (?, ?, ?, ?)
        """, data)
        await db_conn.commit()
    except aiosqlite.OperationalError as e:
        if "locked" in str(e).lower():
            logger.warning("Database locked, background update skipped. It will sync on next request.")
        else:
            logger.error(f"Background DB Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected DB Error: {e}")

async def get_indexed_page(item_id):
    async with db_conn.execute("SELECT page FROM items WHERE id = ?", (item_id,)) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def remove_missing_from_db(item_ids):
    if not item_ids: return
    placeholders = ','.join(['?'] * len(item_ids))
    await db_conn.execute(f"DELETE FROM items WHERE id IN ({placeholders})", item_ids)
    await db_conn.commit()

# -------------------- Fetch Logic --------------------

async def fetch_traderie_page(session, page_num):
    """
    Fetch a single Traderie page from the Node.js Puppeteer service.

    :param session: aiohttp session
    :param page_num: page number to fetch
    :return: tuple (fetch_done, items, version)
    """
    async with scraper_semaphore:
        try:
            async with session.get(
                NODE_SERVICE_URL,
                params={"page": page_num},
                timeout=30
            ) as resp:

                if resp.status != 200:
                    logger.error(f"❌ Node service error on page {page_num}")
                    return True, [], None

                data = await resp.json()

                items = data.get("items", [])
                version = data.get("version")

                if not items:
                    logger.info(f"⚠️ No items on page {page_num}")
                    return True, [], version

                logger.info(f"✅ Page {page_num}: {len(items)} items")
                return False, items, version

        except asyncio.TimeoutError:
            logger.error(f"⏱ Timeout on page {page_num}")
            return True, [], None

        except Exception as e:
            logger.exception(f"❌ Fetch failed on page {page_num}: {e}")
            return True, [], None

async def fetch_multiple_pages(start_page, count):
    all_items = []
    version = None
    fetch_done = False
    items_with_pages = []

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_traderie_page(session, page)
            for page in range(start_page, start_page + count)
        ]

        results = await asyncio.gather(*tasks)

        empty_pages = 0
        for page_offset, (done, items, fetched_version) in enumerate(results):
            page_num = start_page + page_offset
            if items:
                all_items.extend(items)
                items_with_pages.extend([(item, page_num) for item in items])
            else:
                empty_pages += 1

            if fetched_version and not version:
                version = fetched_version

        if empty_pages == count:
            fetch_done = True

    return fetch_done, all_items, version, items_with_pages

# -------------------- Routes --------------------

@app.route("/health", methods=["GET"])
async def health():
    node_status = "unknown"
    status = "ok"
    current_pid = node_process.pid if node_process else None

    if node_process is None or node_process.returncode is not None:
        node_status = "down"
        status = "degraded"
    else:
        # Check if Node is actually responding to HTTP
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(NODE_SERVICE_URL.replace("/traderie", "/health"), timeout=2) as resp:
                    if resp.status == 200:
                        node_status = "ok"
                    else:
                        node_status = "unhealthy"
                        status = "degraded"
        except Exception:
            node_status = "unreachable"
            status = "degraded"

    return jsonify({
        "status": status,
        "node_service": {
            "status": node_status,
            "pid": current_pid,
            "consecutive_failures": node_retries,
            "max_retries_allowed": NODE_MAX_RETRIES
        },
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    })

@app.route("/items", methods=["GET"])
async def get_items():
    all_items = []
    start_page = 0
    version = None
    fetched_ids = set()

    while True:
        fetch_done, items, fetched_version, items_with_pages = await fetch_multiple_pages(start_page, CONCURRENT_PAGES)
        if items:
            all_items.extend(items)
            items_ids = [item.get("id") for item in items if item.get("id")]
            fetched_ids.update(items_ids)
            asyncio.create_task(update_index_db(items_with_pages))

        if fetched_version and not version:
            version = fetched_version

        if fetch_done:
            break

        start_page += CONCURRENT_PAGES

    # Remove any index entries that were not found in the fetched pages
    async with db_conn.execute("SELECT id FROM items") as cursor:
        all_indexed_ids = [row[0] for row in await cursor.fetchall()]

    missing_ids = [id_ for id_ in all_indexed_ids if id_ not in fetched_ids]
    if missing_ids:
        asyncio.create_task(remove_missing_from_db(missing_ids))

    logger.info(f"Returned {len(all_items)} items")
    response = {"items": all_items}
    if version:
        response["version"] = version

    return jsonify(response)

@app.route("/item", methods=["GET"])
async def get_item():
    item_id = request.args.get("id")
    if not item_id:
        return jsonify({"error": "Item id required"}), 400

    version = None
    found_item = None

    # Helper: get page from database
    async def get_indexed_page(item_id):
        async with db_conn.execute("SELECT page FROM items WHERE id = ?", (item_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
            
    start_page = await get_indexed_page(item_id)
        
    async with aiohttp.ClientSession() as session:
        # Fetch indexed page if exists
        if start_page is not None:
            fetch_done, items_chunk, chunk_version, items_with_pages = await fetch_multiple_pages(start_page, 1)
            if chunk_version:
                version = chunk_version
            asyncio.create_task(update_index_db(items_with_pages))
            for item in items_chunk:
                if item.get("id") == item_id:
                    found_item = item
                    break

        # Full search if not found
        if not found_item:
            start_page = 0
            while True:
                fetch_done, items_chunk, chunk_version, items_with_pages = await fetch_multiple_pages(start_page, CONCURRENT_PAGES)
                if chunk_version and not version:
                    version = chunk_version
                asyncio.create_task(update_index_db(items_with_pages))
                for item in items_chunk:
                    if item.get("id") == item_id:
                        found_item = item
                        break
                if found_item or fetch_done:
                    break
                start_page += CONCURRENT_PAGES

        # If still not found, remove from index
        if not found_item and start_page is not None:
            asyncio.create_task(remove_missing_from_db([item_id]))

    if found_item:
        return jsonify({"item": found_item, "version": version})
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route("/node/restart", methods=["POST"])
@require_auth
async def restart_node():
    global node_process, node_retries

    logger.info("Manual restart requested via API.")

    # 1. Stop existing process gracefully
    if node_process and node_process.returncode is None:
        node_process.terminate()
        try:
            # Give it 5 seconds to die gracefully, then force kill if needed
            await asyncio.wait_for(node_process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            node_process.kill()
            await node_process.wait()

    # 2. Reset state
    node_retries = 0 

    # 3. Restart and WAIT for the signal
    try:
        # We call start_node_service directly (it waits for NODE_READY)
        # Wrap in wait_for to prevent the API from hanging forever if Node fails
        await asyncio.wait_for(start_node_service(), timeout=15.0)
        
        return jsonify({
            "status": "success",
            "message": "Node service restarted and ready",
            "new_pid": node_process.pid if node_process else None
        }), 200

    except asyncio.TimeoutError:
        logger.error("Restart timed out: Node service did not signal READY.")
        return jsonify({
            "status": "error",
            "message": "Node service started but timed out waiting for ready signal"
        }), 504
    except Exception as e:
        logger.exception("Failed to restart Node service")
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------- Entry Point --------------------

@app.before_serving
async def startup_tasks():
    await init_db()
    await start_node_service()
    asyncio.create_task(node_watchdog())

@app.after_serving
async def shutdown_tasks():
    stop_node_service()
    if node_process:
        await node_process.wait()
    if db_conn:
        await db_conn.close()

async def main():
    # Start Quart using Hypercorn
    config = Config()
    config.bind = [BIND]
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())






