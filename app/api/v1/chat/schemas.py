from pydantic import BaseModel


class BaseChatMessage(BaseModel):
    message: str


class SendMessageSchema(BaseChatMessage):
    context_id: int = None


class ChatMessageResponseSchema(BaseChatMessage):
    id: int
    sender_type: str
    timestamp: float
    updated_at: float = None


class SendMessageResponseSchema(BaseModel):
    user_message: ChatMessageResponseSchema
    bot_message: ChatMessageResponseSchema


class ChatHistoryResponseSchema(BaseModel):
    messages: list[ChatMessageResponseSchema]


class DeleteMessageSchema(BaseModel):
    message_id: int
    delete_all: bool = False


class UpdateMessageSchema(BaseChatMessage):
    message_id: int


class ChatContextPromptSchema(BaseModel):
    id: int
    title: str
    prompt: str
