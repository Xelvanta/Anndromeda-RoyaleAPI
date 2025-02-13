import json
import subprocess
import time
import os

from quart import Quart, jsonify
from quart_cors import cors

app = Quart(__name__)
cors(app)


async def scrape_traderie(page_num, all_items):  # Accept all_items and new return values
    """
    Scrapes item names and community values from Traderie.com using Puppeteer with Stealth.
    """
    # Construct the command to execute the Javascript file
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traderie_scraper.js")  # Use local script in script
    node_command = ["node", script_path, str(page_num)]  # Use proper path

    try:
        # Execute the Node.js script and capture its output
        process = subprocess.Popen(node_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=60)

        # Check for errors
        if stderr:
            print(f"Error from Node.js script: {stderr.decode()}")
            return True, None  # Stop

        output = stdout.decode()

        # Extract the JSON part
        try:
            start_index = output.find('[')  # JSON starts with '['
            end_index = output.rfind(']') + 1 # and ends with ']'
            json_string = output[start_index:end_index]
        except:
            print(f"Could not parse JSON, raw output: {output}")
            return True, None


        # Parse the JSON output from the Node.js script
        try:
            items = json.loads(json_string)
            print(f"Successfully scraped {len(items)} items from page {page_num}")
            return False, items  # Continue
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Raw output: {json_string}")  # Print the extracted JSON string
            return True, None

    except subprocess.TimeoutExpired:
        print(f"TimeoutExpired: Node.js script timed out on page {page_num}")
        process.kill()  # Ensure the process is terminated
        return True, None  # Error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return True, None  # Catch-all for unanticipated errors during scraping


@app.route('/items', methods=['GET'])
async def get_items():
    all_items = []
    page_number = 0

    scraped_all = False

    while page_number < 100 and not scraped_all:  # Limited to 100 pages for efficiency
        scrape_is_done, new_items = await scrape_traderie(page_number, all_items)
        if scrape_is_done or new_items is None:
            print("No more items or an error occurred. Stopping the scrape.")
            break
        # All items should add
        all_items.extend(new_items)
        # Increase page number
        page_number += 1

    return jsonify(all_items)


if __name__ == '__main__':
    app.run(debug=True)
