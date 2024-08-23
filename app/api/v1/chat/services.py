from fastapi import HTTPException, status
from fastapi.logger import logger
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.chat.models import ChatMessage, SenderType
from app.api.v1.chat.schemas import ChatHistoryResponseSchema, ChatMessageResponseSchema


def generate_system_response(
    message: str,
) -> str:
    """
    Generate a system response.
    """
    return f"System says: {message}"


def process_response_for_chat_message(
    message: ChatMessage,
    session: Session,
) -> ChatMessageResponseSchema:
    """
    Process a chat message response.
    """

    system_message = ChatMessage(
        sender_type=SenderType.SYSTEM,
        user_id=message.user_id,
        message=generate_system_response(
            message=message.message,
        ),
    )

    session.add(system_message)
    session.commit()

    session.refresh(system_message)

    timestamp = system_message.created_at.timestamp()

    return ChatMessageResponseSchema(
        id=system_message.id,
        sender_type=system_message.sender_type.value,
        message=system_message.message,
        timestamp=timestamp,
    )


def receive_chatbot_message(
    user: User,
    message: str,
    session: Session,
) -> ChatMessageResponseSchema:
    """
    Receive a message from the chatbot.
    """
    log_prefix = "[Chatbot Message]"
    logger.info(
        f"{log_prefix} Attempting to send message: {message}",
    )

    chat_message = ChatMessage(
        sender_type=SenderType.USER,
        user_id=user.id,
        message=message,
    )

    session.add(chat_message)
    session.commit()

    return process_response_for_chat_message(
        message=chat_message,
        session=session,
    )


def get_chat_history(
    user: User,
    session: Session,
) -> ChatHistoryResponseSchema:
    """
    Get chat history.
    """
    log_prefix = "[Chat History]"
    logger.info(
        f"{log_prefix} Attempting to get chat history for user: {user.email}",
    )

    chat_messages = (
        session.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id)
        .order_by(ChatMessage.id.asc())
        .all()
    )

    chat_history = [
        ChatMessageResponseSchema(
            id=message.id,
            sender_type=message.sender_type.value,
            message=message.message,
            timestamp=message.created_at.timestamp(),
            updated_at=message.updated_at.timestamp() if message.updated_at else None,
        )
        for message in chat_messages
    ]

    return ChatHistoryResponseSchema(
        messages=chat_history,
    )


def delete_chat_history(
    user: User,
    message_id: int,
    delete_all: bool,
    session: Session,
) -> ChatHistoryResponseSchema:
    """
    Delete chat history.
    """
    log_prefix = "[Chat History]"
    logger.info(
        f"{log_prefix} Attempting to delete chat history for user: {user.email}",
    )

    if delete_all:
        session.query(ChatMessage).filter(ChatMessage.user_id == user.id).delete()
    else:
        session.query(ChatMessage).filter(ChatMessage.id == message_id).delete()

    session.commit()

    return get_chat_history(
        user=user,
        session=session,
    )


def update_chat_message(
    user: User,
    message_id: int,
    new_message: str,
    session: Session,
) -> ChatHistoryResponseSchema:
    """
    Update chat history.
    """
    log_prefix = "[Chat History]"
    logger.info(
        f"{log_prefix} Attempting to update chat history for user: {user.email}",
    )

    chat_message = (
        session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    )

    if not chat_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    chat_message.message = new_message

    session.commit()

    return get_chat_history(
        user=user,
        session=session,
    )
