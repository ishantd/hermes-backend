from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    email: str
    name: str


class UserSignupSchema(BaseUserSchema):
    password: str


class UserResponseSchema(BaseUserSchema):
    user_id: int


class UserLoginSchema(BaseModel):
    email: str
    password: str
