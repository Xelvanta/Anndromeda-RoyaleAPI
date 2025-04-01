import requests
import json
import os
import subprocess
from datetime import datetime, timezone
import pytz

# GitHub authentication
GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USERNAME = "Xelvanta"
REPO_NAME = "RHAPI-items-snapshots"
PRIVATE_REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# API URL
API_URL = "http://127.0.0.1:5000/items"

def get_current_timestamp():
    """
    Returns the current timestamp in the format: YYYY-MM-DD-HH-MM-SS(+/-)HHMM
    """
    now = datetime.now(timezone.utc).astimezone()
    offset = now.strftime("%z")
    formatted_time = now.strftime(f"%Y-%m-%d-%H-%M-%S{offset}-RHAPI")
    return formatted_time

def fetch_items():
    """
    Fetches the items from the /items API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
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
        "description": "Auto-generated Gist from https://github.com/Xelvanta/Anndromeda-RoyaleAPI",
        "public": False,
        "files": {
            filename: {"content": json.dumps(data, indent=2)}
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        gist_url = response.json().get("html_url", "Unknown URL")
        print(f"✅ Gist created: Secret")
    else:
        print(f"❌ Failed to create Gist: {response.text}")

def upload_to_repo(data):
    """
    Saves the JSON file to the snapshots/ directory and pushes it to the private GitHub repository.
    """
    filename = f"items-{get_current_timestamp()}.json"
    repo_path = "/tmp/private_repo"
    snapshots_path = os.path.join(repo_path, "snapshots")

    # Clone the private repo if not already cloned
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", PRIVATE_REPO_URL, repo_path], check=True)

    # Ensure snapshots directory exists
    os.makedirs(snapshots_path, exist_ok=True)

    # Save JSON inside snapshots/
    file_path = os.path.join(snapshots_path, filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    # Commit and push
    subprocess.run(["git", "-C", repo_path, "config", "user.name", "Xelvanta"], check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.email", "187991660+Xelvanta@users.noreply.github.com"], check=True)
    subprocess.run(["git", "-C", repo_path, "add", file_path], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", f"Auto-update {filename}"], check=True)
    subprocess.run(["git", "-C", repo_path, "push"], check=True)

    print(f"✅ File {filename} uploaded to snapshots/ in private repo.")

# Fetch items and process
items = fetch_items()
create_gist(items)
upload_to_repo(items)
