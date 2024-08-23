from pydantic import BaseModel


class BaseChatMessage(BaseModel):
    message: str


class SendMessageSchema(BaseChatMessage):
    pass


class ChatMessageResponseSchema(BaseChatMessage):
    id: int
    sender_type: str
    timestamp: float
    updated_at: float = None


class ChatHistoryResponseSchema(BaseModel):
    messages: list[ChatMessageResponseSchema]


class DeleteMessageSchema(BaseModel):
    message_id: int
    delete_all: bool = False


class UpdateMessageSchema(BaseChatMessage):
    message_id: int
