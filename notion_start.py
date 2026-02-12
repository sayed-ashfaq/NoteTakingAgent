import requests
import os
from dotenv import load_dotenv
load_dotenv()

# ==============================
# CONFIG (Fill these)
# ==============================

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_PAGE_ID")

# ==============================
# HEADERS (Required)
# ==============================

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ==============================
# DATA: Create a new Page
# ==============================

payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {
            "title": [
                {"text": {"content": "My first note from Python"}}
            ]
        }
    }
}

# ==============================
# API Request
# ==============================

response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=payload
)

# ==============================
# Output
# ==============================

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("✅ Page created successfully!")
else:
    print("❌ Error:")
    print(response.json())
