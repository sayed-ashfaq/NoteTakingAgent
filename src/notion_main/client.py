import requests
import os
from dotenv import load_dotenv
load_dotenv()


class NotionClient:
    def __init__(self):
        self.token = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_PAGE_ID")
        self.url = "https://api.notion.com/v1/"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def add_note(self, properties: dict, children: list):
        """
        note_type must be one of: Idea, Task, Note
        """

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": children
        }

        response = requests.post(
            self.url + "pages",
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Notion API Error: {response.json()}")

        return response.json()
