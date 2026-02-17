
import os
import httpx
from datetime import datetime
from app.core.config import settings

class NotionService:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY") 
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.search_url = "https://api.notion.com/v1/search"
        self.pages_url = "https://api.notion.com/v1/pages"
        self.blocks_url = "https://api.notion.com/v1/blocks"
        self.parent_page_id = os.getenv("NOTION_PAGE_ID")

    async def find_page_by_title(self, title: str):
        """Finds a page by its title."""
        payload = {
            "query": title,
            "filter": {
                "property": "object",
                "value": "page"
            },
            "page_size": 1
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.search_url, json=payload, headers=self.headers)
            if response.status_code == 200:
                results = response.json().get("results", [])
                return results[0] if results else None
            return None

    async def add_note(self, properties: dict, children: list):
        """Creates a new page with given properties and content."""
        data = {
            "parent": {"page_id": self.parent_page_id},
            "properties": properties,
            "children": children
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.pages_url, json=data, headers=self.headers)
            if response.status_code != 200:
                raise Exception(f"Notion API Error: {response.text}")
            return response.json()

    async def append_blocks(self, page_id: str, children: list):
        """Appends blocks to an existing page."""
        url = f"{self.blocks_url}/{page_id}/children"
        data = {"children": children}
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data, headers=self.headers)
            if response.status_code != 200:
                raise Exception(f"Notion Error: {response.text}")
            return response.json()

notion_service = NotionService()
