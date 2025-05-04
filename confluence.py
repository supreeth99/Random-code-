import os
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# === CONFIGURATION ===
EMAIL = "your.email@example.com"
API_TOKEN = "your-api-token"
BASE_URL = "https://your-domain.atlassian.net/wiki"
SPACE_KEY = "YOUR_SPACE_KEY"
SAVE_DIR = "confluence_pages"

# === CREATE OUTPUT DIR ===
os.makedirs(SAVE_DIR, exist_ok=True)

# === BASE API ENDPOINT ===
API_URL = f"{BASE_URL}/rest/api/content"
params = {
    "type": "page",
    "spaceKey": SPACE_KEY,
    "limit": 100,
    "expand": "body.storage"
}

# === FETCH AND SAVE PAGES ===
def fetch_and_save_pages():
    next_url = API_URL
    page_number = 1

    while next_url:
        print(f"Fetching pages (batch {page_number})...")
        response = requests.get(next_url, params=params if page_number == 1 else None,
                                auth=HTTPBasicAuth(EMAIL, API_TOKEN))
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        for page in data["results"]:
            title = page["title"]
            content_html = page["body"]["storage"]["value"]
            text = BeautifulSoup(content_html, "html.parser").get_text()

            # Clean filename
            filename = f"{title}".replace("/", "_").replace("\\", "_") + ".txt"
            filepath = os.path.join(SAVE_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved: {title}")

        # Pagination
        next_link = data.get("_links", {}).get("next")
        next_url = BASE_URL + next_link if next_link else None
        page_number += 1

    print("Done!")

# === RUN ===
if __name__ == "__main__":
    fetch_and_save_pages()