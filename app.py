import json
import subprocess
import os

from quart import Quart, jsonify
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
            json_start = stdout_decoded.find("[{")  # Find start of JSON
            json_end = stdout_decoded.rfind("}]") + 2  # Find end of JSON
            json_data = stdout_decoded[json_start:json_end]  # Extract JSON part

            items = json.loads(json_data)  # Load only the JSON
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
    all_items = []
    page_number = 0

    while page_number < 100:
        scrape_done, new_items = await scrape_traderie(page_number)
        if scrape_done or not new_items:
            break
        all_items.extend(new_items)
        page_number += 1

    return jsonify(all_items)

if __name__ == '__main__':
    app.run(debug=True)
