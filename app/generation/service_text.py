from abc import ABC, abstractmethod

from .config import generation_setting

from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


class TextGeneration(ABC):
    @abstractmethod
    def generate_text(self, system_prompt, user_prompt) -> str:
        pass


class GigaChatText(TextGeneration):
    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.parser = StrOutputParser()

    def generate_text(self, system_prompt: str | None, user_prompt: str | None) -> str:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(system_prompt))
        if user_prompt:
            messages.append(HumanMessage(user_prompt))
        response = self.model.invoke(messages)
        return self.parser.invoke(response)
