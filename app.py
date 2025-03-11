import json
import os
import asyncio
import logging
from quart import Quart, jsonify, request
from quart_cors import cors

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

async def scrape_traderie(page_num):
    """
    Scrapes data from a specified page using a Node.js script.
    
    :param page_num: The page number to scrape.
    :return: A tuple containing a boolean indicating if scraping is done and a list of scraped items.
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traderie_scraper.js")
    node_command = ["node", script_path, str(page_num)]

    try:
        process = await asyncio.create_subprocess_exec(
            *node_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stderr:
            logger.warning(f"⚠️ Error from Node.js script (page {page_num}): {stderr.decode()}")
            return True, []

        try:
            stdout_decoded = stdout.decode()
            json_start = stdout_decoded.find("[{")
            json_end = stdout_decoded.rfind("}]") + 2
            json_data = stdout_decoded[json_start:json_end]
            
            items = json.loads(json_data)
            if not items:
                logger.warning(f"⚠️ No items found on page {page_num}.")
                return True, []
            
            logger.info(f"✅ Successfully scraped {len(items)} items from page {page_num}")
            return False, items
        
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ JSON Decoding Error on page {page_num}: {e}, Extracted JSON: {json_data}")
            return True, []
    
    except asyncio.TimeoutError:
        logger.error(f"TimeoutExpired: Node.js script timed out on page {page_num}")
        return True, []

async def scrape_multiple_pages(start_page, end_page):
    """
    Scrapes multiple pages concurrently.
    
    :param start_page: The starting page number.
    :param end_page: The ending page number.
    :return: A tuple containing a boolean indicating if scraping is done and a list of all collected items.
    """
    tasks = [scrape_traderie(page_num) for page_num in range(start_page, end_page)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items = []
    scrape_done = False

    for result in results:
        if isinstance(result, Exception):
            logger.error(f"⚠️ Exception during scraping: {result}")
            scrape_done = True
            continue
        
        scrape_status, new_items = result
        if scrape_status:
            scrape_done = True
            continue

        if new_items:
            all_items.extend(new_items)

    return scrape_done, all_items

def remove_duplicates(items):
    """
    Removes duplicate items based on their 'name' field, keeping the first occurrence.
    """
    seen = set()
    unique_items = []
    for item in items:
        if item['name'] not in seen:
            unique_items.append(item)
            seen.add(item['name'])
    return unique_items

@app.route('/items', methods=['GET'])
async def get_items():
    """
    Endpoint to fetch all scraped items by scraping multiple pages.
    """
    all_items = []
    start_page = 0
    end_page = concurrent_pages

    while True:
        scrape_done, scrape_results = await scrape_multiple_pages(start_page, end_page)
        all_items.extend(scrape_results)
        
        if scrape_done:
            break

        start_page = end_page
        end_page += concurrent_pages
    
    all_items = remove_duplicates(all_items)
    logger.info(f"Returned {len(all_items)} items after removing duplicates")
    
    return jsonify(all_items)

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
        scrape_done, new_items = await scrape_traderie(page_number)
        if scrape_done or not new_items:
            break

        for item in new_items:
            if item.get("name") == item_name:
                return jsonify({"value": item.get("value")})
        
        page_number += 1
    
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
