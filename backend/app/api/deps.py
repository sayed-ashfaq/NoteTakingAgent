
from typing import Generator
from fastapi import Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user_id
from app.models.user import User

def get_db() -> Generator[Session, None, None]:
    yield from get_session()

def get_current_user(
    db: Session = Depends(get_db),
    clerk_id: str = Depends(get_current_user_id)
) -> User:
    # First, try to find user in our local DB
    user = db.query(User).filter(User.clerk_id == clerk_id).first()
    
    # If using Clerk, we might want to auto-create user on first login
    if not user:
        user = User(clerk_id=clerk_id, email=f"{clerk_id}@clerk.dev") # Placeholder email
        db.add(user)
        db.commit()
        db.refresh(user)
        
    return user
