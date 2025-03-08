import json
import os
import asyncio
from quart import Quart, jsonify, request
from quart_cors import cors

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
        # Execute the Node.js script
        process = await asyncio.create_subprocess_exec(
            *node_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:
            print(f"⚠️ Error from Node.js script (page {page_num}): {stderr.decode()}")
            return True, []

        try:
            # Decode and extract JSON data from the output
            stdout_decoded = stdout.decode()
            json_start = stdout_decoded.find("[{")
            json_end = stdout_decoded.rfind("}]") + 2
            json_data = stdout_decoded[json_start:json_end]

            items = json.loads(json_data)
            if not items:
                print(f"⚠️ No items found on page {page_num}.")
                return True, []  # Return True and empty list if no items found

            print(f"✅ Successfully scraped {len(items)} items from page {page_num}")
            return False, items  # Return False (not done) and the scraped items

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Decoding Error on page {page_num}: {e}, Extracted JSON: {json_data}")
            return True, []  # Return True (done) and empty list on error

    except asyncio.TimeoutError:
        print(f"⏳ TimeoutExpired: Node.js script timed out on page {page_num}")
        return True, []  # Return True and empty list if timed out

async def scrape_multiple_pages(start_page, end_page):
    """
    Scrapes multiple pages concurrently.

    :param start_page: The starting page number.
    :param end_page: The ending page number.
    :return: A tuple containing a boolean indicating if scraping is done and a list of all collected items.
    """
    tasks = []
    for page_num in range(start_page, end_page):
        tasks.append(scrape_traderie(page_num))  # Add each scrape task to the list

    # Run all scrape tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)  # Capture exceptions

    all_items = []
    scrape_done = False  # Flag to track whether an invalid page was found

    for result in results:
        if isinstance(result, Exception):
            # Handle exceptions raised during scraping
            print(f"⚠️ Exception during scraping: {result}")
            scrape_done = True
            continue
        
        scrape_status, new_items = result
        if scrape_status:  # If there's an error with scraping this page (invalid), mark it as invalid but continue
            scrape_done = True  # Mark the batch as invalid (stop further processing)
            continue  # Continue processing other pages even if one fails

        if new_items:  # Only add items if the list is not empty
            all_items.extend(new_items)

    return scrape_done, all_items  # Return both status (if any page failed) and collected items

@app.route('/items', methods=['GET'])
async def get_items():
    """
    Endpoint to fetch all scraped items by scraping multiple pages.

    :return: A JSON response containing all the scraped items.
    """
    all_items = []
    start_page = 0
    end_page = concurrent_pages  # Use the value from the config file

    while True:
        scrape_done, scrape_results = await scrape_multiple_pages(start_page, end_page)

        # Collect valid items from this batch
        all_items.extend(scrape_results)

        # If any page in the batch was invalid, stop processing more batches
        if scrape_done:
            break

        start_page = end_page
        end_page += concurrent_pages  # Move the page range forward for the next set of pages

    return jsonify(all_items)

@app.route('/item', methods=['GET'])
async def get_item_value():
    """
    Endpoint to fetch the value of a specific item by name.

    :return: A JSON response containing the item's value or an error if not found.
    """
    item_name = request.args.get("name")  # Get item name from query params

    if not item_name:
        return jsonify({"error": "Item name is required"}), 400  # Bad Request if no 'name' parameter

    page_number = 0
    while True:
        scrape_done, new_items = await scrape_traderie(page_number)
        if scrape_done or not new_items:
            break

        for item in new_items:
            if item.get("name") == item_name:
                return jsonify({"value": item.get("value")})  # Return value immediately

        page_number += 1

    return jsonify({"error": "Item not found"}), 404  # If no match found in all pages

if __name__ == '__main__':
    app.run(debug=True)
