import json
import os
import asyncio
import logging
from quart import Quart, jsonify, request
from quart_cors import cors

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Quart(__name__)
cors(app)

def load_config():
    """
    Loads the configuration from the config.json file.
    
    :return: Parsed JSON configuration.
    """
    with open('config.json') as f:
        return json.load(f)

config = load_config()
concurrent_pages = config['concurrent_pages']

async def fetch_traderie_data(page_num):
    """
    Fetches data from the Traderie API using the fetchData.js Node.js script.
    
    :param page_num: The page number to fetch data for.
    :return: A tuple containing a boolean indicating if fetching is done and a list of fetched items.
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetchData.js")
    node_command = ["node", script_path, str(page_num)]

    try:
        process = await asyncio.create_subprocess_exec(
            *node_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stderr:
            logger.warning(f"⚠️ Error from Node.js script (page {page_num}): {stderr.decode()}")
            return True, [], None

        try:
            data = json.loads(stdout.decode())

            if not data or "items" not in data:
                logger.warning(f"⚠️ Invalid response format on page {page_num}: {data}")
                return True, [], None

            # Handle cases where 'items' is inside another dictionary
            if isinstance(data['items'], dict):  
                items = data['items'].get('items', [])  # Extract the actual list of items
                version = data['items'].get('version')  # Extract version if available
            else:
                items = data['items']
                version = data.get('version')

            if not isinstance(items, list) or not items:
                logger.warning(f"⚠️ No valid items found on page {page_num}. Response: {data}")
                return True, [], version

            logger.info(f"✅ Successfully fetched {len(items)} items from page {page_num}")
            return False, items, version

        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ JSON Decoding Error on page {page_num}: {e}")
            logger.warning(f"Extracted JSON: {stdout.decode()}")
            return True, [], None
    
    except asyncio.TimeoutError:
        logger.error(f"TimeoutExpired: Node.js script timed out on page {page_num}")
        return True, [], None

async def fetch_multiple_pages(start_page, end_page):
    """
    Fetches multiple pages concurrently from the Traderie API.
    
    :param start_page: The starting page number.
    :param end_page: The ending page number.
    :return: A tuple containing a boolean indicating if fetching is done and a list of all collected items.
    """
    tasks = [fetch_traderie_data(page_num) for page_num in range(start_page, end_page)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items = []
    fetch_done = False
    version = None

    for result in results:
        if isinstance(result, Exception):
            logger.error(f"⚠️ Exception during fetching: {result}")
            fetch_done = True
            continue
        
        fetch_status, new_items, fetched_version = result
        if fetch_status:
            fetch_done = True
            continue

        if new_items:
            all_items.extend(new_items)

        if fetched_version and not version:
            version = fetched_version

    return fetch_done, all_items, version

@app.route('/items', methods=['GET'])
async def get_items():
    """
    Endpoint to fetch all fetched items by fetching multiple pages.
    """
    all_items = []
    start_page = 0
    end_page = concurrent_pages
    version = None

    while True:
        fetch_done, fetch_results, fetched_version = await fetch_multiple_pages(start_page, end_page)

        if fetch_results:
            all_items.extend(fetch_results)

        if fetched_version and not version:
            version = fetched_version

        if fetch_done:
            break

        start_page = end_page
        end_page += concurrent_pages

    response_data = {"items": all_items}
    if version:
        response_data["version"] = version

    logger.info(f"Returned {len(all_items)} items, version {version}")

    return jsonify(response_data)

@app.route('/item', methods=['GET'])
async def get_item_value():
    """
    Endpoint to fetch the value of a specific item by name.
    """
    item_name = request.args.get("name")
    if not item_name:
        return jsonify({"error": "Item name is required"}), 400
    
    page_number = 0
    while True:
        fetch_done, new_items, _ = await fetch_traderie_data(page_number)
        if fetch_done or not new_items:
            break

        for item in new_items:
            if item.get("name") == item_name:
                if item.get('prices') and len(item.get('prices')) > 0:
                    return jsonify({"value": item['prices'][0].get('user_value')}) # Use user value if there is a price
                else:
                    return jsonify({"value": None}) # If no price available return none
        
        page_number += 1
    
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
