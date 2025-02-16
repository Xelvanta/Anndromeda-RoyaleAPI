import json
import subprocess
import os

from quart import Quart, jsonify, request
from quart_cors import cors

app = Quart(__name__)
cors(app)

async def scrape_traderie(page_num):
    """
    Scrapes item names and community values from Traderie.com using Puppeteer.
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traderie_scraper.js")
    node_command = ["node", script_path, str(page_num)]

    try:
        process = subprocess.Popen(node_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=60)

        if stderr:
            print(f"⚠️ Error from Node.js script: {stderr.decode()}")
            return True, []

        try:
            stdout_decoded = stdout.decode()
            json_start = stdout_decoded.find("[{")  
            json_end = stdout_decoded.rfind("}]") + 2  
            json_data = stdout_decoded[json_start:json_end]  

            items = json.loads(json_data)  
            if not items:
                print(f"⚠️ No items found on page {page_num}.")
                return True, []
            print(f"✅ Successfully scraped {len(items)} items from page {page_num}")
            return False, items

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Decoding Error: {e}, Extracted JSON: {json_data}")
            return True, []

    except subprocess.TimeoutExpired:
        print(f"⏳ TimeoutExpired: Node.js script timed out on page {page_num}")
        process.kill()
        return True, []

@app.route('/items', methods=['GET'])
async def get_items():
    """Fetch all items."""
    all_items = []
    page_number = 0

    while True:  # Infinite loop until we get no items
        scrape_done, new_items = await scrape_traderie(page_number)
        if scrape_done or not new_items:
            break
        all_items.extend(new_items)
        page_number += 1

    return jsonify(all_items)

@app.route('/item', methods=['GET'])
async def get_item_value():
    """Fetch the value of a specific item based on the query parameter."""
    item_name = request.args.get("name")  # Get item name from query params

    # If no 'name' query parameter, return all items
    if not item_name:
        all_items = []
        page_number = 0

        while True:  # Infinite loop until we get no items
            scrape_done, new_items = await scrape_traderie(page_number)
            if scrape_done or not new_items:
                break
            all_items.extend(new_items)
            page_number += 1

        return jsonify(all_items)  # Return all items if no 'name' query parameter

    # If 'name' is provided, return the value of the specific item
    page_number = 0
    while True:  # Infinite loop until we get no items
        scrape_done, new_items = await scrape_traderie(page_number)
        if scrape_done or not new_items:
            break

        # Search for the item in the current page
        for item in new_items:
            if item.get("name") == item_name:
                return jsonify({"value": item.get("value")})  # Return value immediately

        page_number += 1

    return jsonify({"error": "Item not found"}), 404  # If no match found in all pages

if __name__ == '__main__':
    app.run(debug=True)
