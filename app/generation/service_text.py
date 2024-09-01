from abc import ABC, abstractmethod

from .config import generation_setting

from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models.gigachat import GigaChat
from langchain_community.chat_models import ChatYandexGPT
import requests

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


class YandexGPTTextGiga(TextGeneration):
    def __init__(self):
        self.model = ChatYandexGPT(api_key=generation_setting.yandexchat_api_key, folder_id=generation_setting.yandexchat_folder_id)
        self.parser = StrOutputParser()

    def generate_text(self, prompt: list[message_type]) -> str:
        response = self.model.invoke(prompt)
        return self.parser.invoke(response)

class YandexGPTTextRequests(TextGeneration):
    def __init__(self):
        self.api_key = generation_setting.yandexchat_api_key.get_secret_value()
        self.folder_id = generation_setting.yandexchat_folder_id
        self.model_uri = 'yandexgpt-lite/latest'
        self.max_tokens = 500
        self.temperature = 1

    def _create_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Api-Key '+self.api_key
        }
    
    def _create_payload(self, messages: list[dict[str, str]]):
        return {
            "modelUri": "gpt://"+self.folder_id+"/"+self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": self.temperature,
                "maxTokens": self.max_tokens
            },
            "messages": messages
        }

    def generate_text(self, prompt: list[message_type], url_to_server: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion') -> str:
        messages = []
        for x in prompt:
            if x.type == 'ai':
                messages.append({
                    "role": "assistant",
                    "text": x.content
                })
            elif x.type == 'human':
                messages.append({
                    "role": "user",
                    "text": x.content
                })
            else:
                messages.append({
                    "role": "system",
                    "text": x.content
                })
        answer = requests.post(url_to_server, headers=self._create_header(), json=self._create_payload(messages))
        answer_json = answer.json()
        print(answer_json)
        generated_text = answer_json['result']['alternatives'][0]['message']['text']
        totalTokens = answer_json['result']['usage']['totalTokens']
        return generated_text

text_generation_model = YandexGPTTextRequests()
