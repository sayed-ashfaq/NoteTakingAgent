import requests
import os
from dotenv import load_dotenv
import datetime
from utils.data_parsing import markdown_to_notion_blocks
load_dotenv()


# ==============================
# CONFIG (Fill these)
# ==============================

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_PAGE_ID")
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

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
# children = parse_data("data//test_data.md")
children = markdown_to_notion_blocks("data//test_data2.md")

payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {
            "title": [
                {"text": {"content": "Testing Notion API 2"}}
            ]
        },
        "Tags": {
            "multi_select": [
                { "name": "Tag1" },
                { "name": "Tag2" }
            ]
        },
        "Date": {
            "date": {
                "start": current_date
            }
        },
        "Status": {
            "select": {"name": "In Progress"}
        },
    },
    'children': children    
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
