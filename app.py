"""
app.py

Quart-based API that fetches Traderie item data by calling
a long-lived Puppeteer Node.js service over HTTP.

This design avoids subprocess spawning and enables efficient
concurrent scraping with preserved browser state.
"""

import asyncio
import atexit
import json
import logging
import os
import signal
import sys
import aiohttp
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, jsonify, request
from quart_cors import cors

# -------------------- Logging --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- App Setup --------------------

app = Quart(__name__)
cors(app)

CONCURRENT_PAGES = 5

# ------------------ Node Service -----------------

NODE_SCRIPT = os.path.join(os.path.dirname(__file__), "fetchData.js")
NODE_SERVICE_URL = "http://localhost:3001/traderie"

node_process = None

async def start_node_service():
    global node_process
    node_command = ["node", NODE_SCRIPT]

    node_process = await asyncio.create_subprocess_exec(
        *node_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for NODE_READY line
    while True:
        line = await node_process.stdout.readline()
        if not line:
            await asyncio.sleep(0.1)
            continue
        decoded = line.decode().strip()
        print(f"[Node stdout] {decoded}")
        if decoded == "NODE_READY":
            print("✅ Node signaled ready")
            break

def stop_node_service():
    """
    Ensures the Node.js process is terminated on Python exit.
    """
    global node_process
    if node_process and node_process.returncode is None:
        print("🛑 Stopping Node.js service...")
        node_process.send_signal(signal.SIGINT)

# Register shutdown handler
atexit.register(stop_node_service)

# ------------------- Item Indexing -------------------

INDEX_FILE = os.path.join(os.path.dirname(__file__), "item_index.json")

# Load the index from disk, or initialize empty
def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save the index to disk
def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

# Update index for a list of items
def update_index(items_with_pages, index):
    for item, page_num in items_with_pages:
        name = item.get("name")
        item_id = item.get("id")
        if name and item_id:
            if name not in index:
                index[name] = []
            # Only append if this id is not already indexed
            if not any(entry["id"] == item_id for entry in index[name]):
                index[name].append({"id": item_id, "page": page_num})
    save_index(index)

def remove_missing_from_index(missing_ids, index):
    """Remove items with IDs in missing_ids from the index."""
    changed = False
    for name in list(index.keys()):
        new_entries = [e for e in index[name] if e.get("id") not in missing_ids]
        if len(new_entries) != len(index[name]):
            index[name] = new_entries
            changed = True
        if not index[name]:
            del index[name]
    if changed:
        save_index(index)

# -------------------- Fetch Logic --------------------

async def fetch_traderie_page(session, page_num):
    """
    Fetch a single Traderie page from the Node.js Puppeteer service.

    :param session: aiohttp session
    :param page_num: page number to fetch
    :return: tuple (fetch_done, items, version)
    """
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

@app.route("/items", methods=["GET"])
async def get_items():
    all_items = []
    start_page = 0
    version = None
    index = load_index()
    fetched_ids = set()

    while True:
        fetch_done, items, fetched_version, items_with_pages = await fetch_multiple_pages(start_page, CONCURRENT_PAGES)
        if items:
            all_items.extend(items)
            items_ids = [item.get("id") for item in items if item.get("id")]
            fetched_ids.update(items_ids)
            update_index(items_with_pages, index)

        if fetched_version and not version:
            version = fetched_version

        if fetch_done:
            break

        start_page += CONCURRENT_PAGES

    # Remove any index entries that were not found in the fetched pages
    all_indexed_ids = [e["id"] for entries in index.values() for e in entries]
    missing_ids = [id_ for id_ in all_indexed_ids if id_ not in fetched_ids]
    if missing_ids:
        remove_missing_from_index(missing_ids, index)

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

    index = load_index()
    version = None
    found_item = None

    # Helper: get page from index
    def get_indexed_page():
        for entries in index.values():
            for entry in entries:
                if entry.get("id") == item_id:
                    return entry.get("page", 0)
        return None

    start_page = get_indexed_page()
    async with aiohttp.ClientSession() as session:

        # Fetch indexed page if exists
        if start_page is not None:
            fetch_done, items_chunk, chunk_version, items_with_pages = await fetch_multiple_pages(start_page, 1)
            if chunk_version:
                version = chunk_version
            update_index(items_with_pages, index)
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
                update_index(items_with_pages, index)
                for item in items_chunk:
                    if item.get("id") == item_id:
                        found_item = item
                        break
                if found_item or fetch_done:
                    break
                start_page += CONCURRENT_PAGES

        # If still not found, remove from index
        if not found_item and start_page is not None:
            remove_missing_from_index([item_id], index)

    if found_item:
        return jsonify({"item": found_item, "version": version})
    else:
        return jsonify({"error": "Item not found"}), 404

# -------------------- Entry Point --------------------

async def main():
    # 1. Start Node service
    await start_node_service()

    # 2. Start Quart using Hypercorn (async)
    config = Config()
    config.bind = ["127.0.0.1:5000"]  # or your port
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
