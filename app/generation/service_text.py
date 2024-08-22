from abc import ABC, abstractmethod

from .config import generation_setting

from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models.gigachat import GigaChat
from langchain_community.chat_models import ChatYandexGPT

message_type = HumanMessage | SystemMessage | AIMessage


class TextGeneration(ABC):
    @abstractmethod
    def generate_text(self, prompt: list[message_type]) -> str:
        pass


class GigaChatText(TextGeneration):
    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.parser = StrOutputParser()

    def generate_text(self, prompt: list[message_type]) -> str:
        response = self.model.invoke(prompt)
        return self.parser.invoke(response)


class YandexGPTText(TextGeneration):
    def __init__(self):
        self.model = ChatYandexGPT(api_key=generation_setting.yandexchat_api_key, folder_id=generation_setting.yandexchat_folder_id)
        self.parser = StrOutputParser()

    def generate_text(self, prompt: list[message_type]) -> str:
        response = self.model.invoke(prompt)
        return self.parser.invoke(response)


text_generation_model = GigaChatText()
