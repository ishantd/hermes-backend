from fastapi.logger import logger
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.chat.models import ChatMessage, SenderType
from app.api.v1.chat.schemas import ChatMessageResponseSchema


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

    return ChatMessageResponseSchema(
        id=system_message.id,
        sender_type=system_message.sender_type.value,
        message=system_message.message,
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
