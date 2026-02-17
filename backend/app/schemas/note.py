
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class NoteProcessRequest(BaseModel):
    text: str
    audio_file: Optional[bytes] = None # Or upload file logic

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    category: str
    target_date: Optional[str]
    tags: List[str]
    created_at: datetime
    owner_id: str

class ProcessedNote(BaseModel):
    category: str
    title: str
    formatted_content: str
    properties: dict
    status: str
    target_date: str
    tags: List[str]
