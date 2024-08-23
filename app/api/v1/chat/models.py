import enum

from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from app.database import Base


class SenderType(enum.Enum):
    """
    Enum for sender type.
    """

    USER = "USER"
    SYSTEM = "SYSTEM"


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True)
    sender_type = Column(Enum(SenderType), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(String, nullable=False)
