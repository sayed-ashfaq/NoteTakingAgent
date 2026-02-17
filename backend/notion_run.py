##  Create Notion Client

from src.notion_main.client import NotionClient
from utils.data_parsing import markdown_to_notion_blocks
from datetime import datetime


client = NotionClient()

properties = {
        "Name": {
            "title": [
                {"text": {"content": "Testing Notion Client"}}
            ]
        },
        "Tags": {
            "multi_select": [
                { "name": "TestingTag1" },
                { "name": "TestingTag2" }
            ]
        },
        "Date": {
            "date": {
                "start": datetime.now().strftime("%Y-%m-%d")
            }
        },
        "Status": {
            "select": {"name": "In Progress"}
        },
    }

children = markdown_to_notion_blocks("data//test_data2.md")

client.add_note(properties, children) # This is how it works 

