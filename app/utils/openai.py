from openai import OpenAI

from app.constants import SYSTEM_CHATBOT_PROMPT
from app.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


def get_response_from_gpt(message: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_CHATBOT_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content


def get_response_from_gpt_with_context(messages: list) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return completion.choices[0].message.content
