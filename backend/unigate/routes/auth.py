from typing import TypedDict

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from unigate.core.database import get_session
from unigate.models.student import Student

router = APIRouter()


class CurrentUserInfo(TypedDict):
    id: str
    name: str
    email: str
    is_authenticated: bool


# TODO
@router.get("", response_model=CurrentUserInfo)
async def get_current_user(
    user_id: str, session: Session = Depends(get_session)
) -> CurrentUserInfo:
    # Fetch details about the currently authenticated user.
    statement = select(Student).where(Student.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "is_authenticated": True,
    }
