import requests
import json
import os
from datetime import datetime, timezone
import pytz

GITHUB_TOKEN = os.getenv("GH_TOKEN")
API_URL = "http://127.0.0.1:5000/items"

def get_current_timestamp():
    """
    Returns the current timestamp in the format: YYYY-MM-DD-HH-MM-SS(+/-)HHMM
    """
    now = datetime.now(timezone.utc).astimezone()  # Get local time with timezone
    offset = now.strftime("%z")  # Timezone offset in +/-HHMM format
    formatted_time = now.strftime(f"%Y-%m-%d-%H-%M-%S{offset}-RHAPI")
    return formatted_time

def fetch_items():
    """
    Fetches the items from the /items API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching items: {e}")
        return {"error": "Failed to fetch items"}

def create_gist(data):
    """
    Creates a new GitHub Gist with the fetched items.
    """
    filename = f"items-{get_current_timestamp()}.json"
    url = "https://api.github.com/gists"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {
        "description": "Auto-generated Gist from RHAPI",
        "public": True,  # Set to False for private Gists
        "files": {
            filename: {
                "content": json.dumps(data, indent=2)
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        gist_url = response.json().get("html_url", "Unknown URL")
        print(f"✅ Gist created: {gist_url}")
    else:
        print(f"❌ Failed to create Gist: {response.text}")

# Fetch items from API and create Gist
items = fetch_items()
create_gist(items)
