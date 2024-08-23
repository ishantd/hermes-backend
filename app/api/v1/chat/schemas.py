from pydantic import BaseModel


class BaseChatMessage(BaseModel):
    message: str


class SendMessageSchema(BaseChatMessage):
    pass


class ChatMessageResponseSchema(BaseChatMessage):
    id: int
    sender_type: str
    timestamp: float


class ChatHistoryResponseSchema(BaseModel):
    messages: list[ChatMessageResponseSchema]
