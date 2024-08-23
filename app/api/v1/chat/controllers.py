from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.auth.services import get_current_user
from app.api.v1.chat import services
from app.api.v1.chat.schemas import (
    ChatHistoryResponseSchema,
    ChatMessageResponseSchema,
    DeleteMessageSchema,
    SendMessageSchema,
    UpdateMessageSchema,
)
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


@router.get("/history")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(db),
) -> ChatHistoryResponseSchema:
    """
    Get chat history.
    """

    response = services.get_chat_history(
        user=current_user,
        session=session,
    )

    return response


@router.put("/update")
def update_chat_history(
    payload: UpdateMessageSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(db),
) -> ChatHistoryResponseSchema:
    """
    Update chat history.
    """

    try:
        if not payload.message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty.",
            )

        response = services.update_chat_message(
            user=current_user,
            message_id=payload.message_id,
            new_message=payload.message,
            session=session,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return response


@router.delete("/delete")
def delete_chat_history(
    payload: DeleteMessageSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(db),
) -> ChatHistoryResponseSchema:
    """
    Delete chat history.
    """

    response = services.delete_chat_history(
        user=current_user,
        message_id=payload.message_id,
        delete_all=payload.delete_all,
        session=session,
    )

    return response
