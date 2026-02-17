
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, JSON

class NoteBase(SQLModel):
    title: str
    content: str
    status: str = "Active"
    category: str # Note, Idea, Task
    target_date: Optional[str] = None # YYYY-MM-DD
    tags: List[str] = Field(default=[], sa_type=JSON) 

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: str = Field(index=True) # Clerk User ID

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    owner_id: str
