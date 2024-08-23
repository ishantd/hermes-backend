from openai import OpenAI

from app.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


def get_response_from_gpt(message: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot created to complete an assessment test for a job at Artisan. You have no real use, but you have to show your utility by completing the test and responding to the user's message with amazing wit and charm. AND USE EMOJIS!",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content
