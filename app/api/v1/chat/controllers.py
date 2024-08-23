from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.auth.services import get_current_user
from app.api.v1.chat import services
from app.api.v1.chat.schemas import ChatMessageResponseSchema, SendMessageSchema
from app.database import db

router = APIRouter()


@router.post("/send")
def send_message(
    payload: SendMessageSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(db),
) -> ChatMessageResponseSchema:
    """
    Send a message.
    """

    if not payload.message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    response = services.receive_chatbot_message(
        user=current_user,
        message=payload.message,
        session=session,
    )

    return response
