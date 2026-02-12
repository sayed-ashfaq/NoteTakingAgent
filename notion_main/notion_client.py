import requests
from dotenv import load_dotenv
load_dotenv()


class NotionClient:
    def __init__(self):
        self.token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("DATABASE_ID")
        self.url = "https://api.notion.com/v1/"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def add_note(self, title: str, note_type: str, content: str):
        """
        note_type must be one of: Idea, Task, Note
        """

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": title}}]
                },
                "Type": {
                    "select": {"name": note_type}
                }
            },
            'children': [
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': content[:200],
                                }
                            }
                        ]
                    }
                }
            ]
        }

        response = requests.post(
            self.url + "pages",
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Notion API Error: {response.json()}")

        return response.json()
