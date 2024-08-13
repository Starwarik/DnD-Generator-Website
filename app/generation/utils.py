"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from .config import generation_setting

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

while(True):
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    print("Bot: ", res.content)