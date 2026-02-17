
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session
from app.api import deps
from app.models.user import User
from app.models.note import Note
from app.schemas.note import ProcessedNote
from app.services.llm_service import LLMService
from app.services.notion_service import notion_service
from app.services.voice_service import voice_service
from app.utils.data_parsing import markdown_to_notion_blocks

router = APIRouter()

@router.post("/process", response_model=ProcessedNote)
async def process_note(
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Process text or audio input. 
    1. Transcribe audio if present.
    2. Process text with LLM.
    3. Sync to Notion.
    4. Save to local DB.
    """
    
    if not text and not audio:
        raise HTTPException(status_code=400, detail="Either text or audio must be provided")

    input_text = text or ""

    # 1. Handle Audio
    if audio:
        contents = await audio.read()
        transcribed_text = voice_service.transcribe(contents)
        if transcribed_text:
            input_text += f"\n{transcribed_text}" if input_text else transcribed_text

    if not input_text:
        raise HTTPException(status_code=400, detail="Could not extract text from input")

    # 2. LLM Processing
    llm_service = LLMService()
    try:
        processed_note = llm_service.process_text(input_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Processing failed: {str(e)}")

    # 3. Save to Notion
    try:
        children = markdown_to_notion_blocks(processed_note.formatted_content)
        
        # Determine Notion logic
        page_title = ""
        is_append = False
        
        if processed_note.category == "Note":
             page_title = f"Daily Note - {processed_note.target_date}"
             existing_page = await notion_service.find_page_by_title(page_title)
             if existing_page:
                 await notion_service.append_blocks(existing_page["id"], children)
                 is_append = True
             else:
                 await notion_service.add_note(processed_note.properties, children)
                 
        elif processed_note.category == "Task":
             page_title = f"Tasks - {processed_note.target_date}"
             existing_page = await notion_service.find_page_by_title(page_title)
             if existing_page:
                 await notion_service.append_blocks(existing_page["id"], children)
                 is_append = True
             else:
                 # Create container page properties
                 props = processed_note.properties.copy()
                 props["Name"] = {"title": [{"text": {"content": page_title}}]}
                 await notion_service.add_note(props, children)

        else: # Idea
             await notion_service.add_note(processed_note.properties, children)

    except Exception as e:
        # Log error but maybe don't fail request? Or ensure atomicity?
        # For now, simplistic approach
        raise HTTPException(status_code=502, detail=f"Notion Sync failed: {str(e)}")

    # 4. Save to Local DB (for history)
    # We store the *result*, not just raw input
    db_note = Note(
        title=processed_note.title,
        content=processed_note.formatted_content,
        status=processed_note.status,
        category=processed_note.category,
        target_date=processed_note.target_date,
        tags=processed_note.tags,
        owner_id=current_user.clerk_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return processed_note
