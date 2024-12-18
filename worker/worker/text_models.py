from abc import ABC, abstractmethod

import aiohttp

from schemas import (
    Message,
    MessageType,
    TextGenerationResult,
    SpentedTokensCounts,
)
import requests

from typing import Any, final
from config import generation_setting


class TextGenerationModel(ABC):
    """
    Абстрактный класс модели для генерации картинок.
    """

    @abstractmethod
    def generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        raise NotImplementedError()

    @abstractmethod
    async def async_generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        raise NotImplementedError()


'''
@final
class GigaChatText(TextGenerationModel):
    """
    Класс модели для генерации текстов с Гигачатом.
    """

    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.parser = StrOutputParser()

    def _convert_messages(self, prompts: list[Message]) -> list[message_type]:
        messages: list[message_type] = []
        for prompt in prompts:
            match prompt.type:
                case MessageType.assistant:
                    messages.append(AIMessage(prompt.content))
                case MessageType.user:
                    messages.append(HumanMessage(prompt.content))
                case MessageType.system:
                    messages.append(SystemMessage(prompt.content))
        return messages

    def generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        messages = self._convert_messages(prompts)
        response = self.model.invoke(messages)
        count_token = SpentedTokensCounts(
            gigachat_prompt_token_count=response.response_metadata[
                "token_usage"
            ].prompt_tokens,
            gigachat_assistant_token_count=response.response_metadata[
                "token_usage"
            ].completion_tokens,
        )
        return TextGenerationResult(content=response.content, count_tokens=count_token)

    async def async_generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        messages = self._convert_messages(prompts)
        response = await self.model.ainvoke(messages)
        count_token = SpentedTokensCounts(
            gigachat_prompt_token_count=response.response_metadata[
                "token_usage"
            ].prompt_tokens,
            gigachat_assistant_token_count=response.response_metadata[
                "token_usage"
            ].completion_tokens,
        )
        return TextGenerationResult(content=response.content, count_tokens=count_token)
'''


@final
class YandexGPTTextSync(TextGenerationModel):
    """
    Класс модели для генерации текстов с ЯндексГПТ в синхроном режиме.
    """

    def __init__(
        self,
        url_to_server: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    ):
        self.url_to_server = url_to_server
        self.api_key = generation_setting.yandexchat_api_key.get_secret_value()
        self.folder_id = generation_setting.yandexchat_folder_id
        self.model_uri = "yandexgpt-lite/latest"
        self.max_tokens = 2000
        self.temperature = 1

    def _create_header(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": "Api-Key " + self.api_key,
        }

    def _create_payload(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        return {
            "modelUri": "gpt://" + self.folder_id + "/" + self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": self.temperature,
                "maxTokens": self.max_tokens,
            },
            "messages": messages,
        }

    def _convert_messages(self, prompts: list[Message]) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        for prompt in prompts:
            match prompt.type:
                case MessageType.assistant:
                    messages.append({"role": "assistant", "text": prompt.content})
                case MessageType.user:
                    messages.append({"role": "user", "text": prompt.content})
                case MessageType.system:
                    messages.append({"role": "user", "text": prompt.content})
        return messages

    def generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        messages = self._convert_messages(prompts)
        answer = requests.post(
            self.url_to_server,
            headers=self._create_header(),
            json=self._create_payload(messages),
        )
        answer_json = answer.json()
        count_token = SpentedTokensCounts(
            yandexgpt_prompt_token_count=answer_json["result"]["usage"][
                "inputTextTokens"
            ],
            yandexgpt_assistant_token_count=answer_json["result"]["usage"][
                "completionTokens"
            ],
        )
        return TextGenerationResult(
            content=answer_json["result"]["alternatives"][0]["message"]["text"],
            count_tokens=count_token,
        )

    async def async_generate_text(self, prompts: list[Message]) -> TextGenerationResult:
        messages = self._convert_messages(prompts)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url_to_server,
                headers=self._create_header(),
                json=self._create_payload(messages),
            ) as resp:
                answer_json = await resp.json()
        count_token = SpentedTokensCounts(
            yandexgpt_prompt_token_count=answer_json["result"]["usage"][
                "inputTextTokens"
            ],
            yandexgpt_assistant_token_count=answer_json["result"]["usage"][
                "completionTokens"
            ],
        )
        return TextGenerationResult(
            content=answer_json["result"]["alternatives"][0]["message"]["text"],
            count_tokens=count_token,
        )


text_generation_model = YandexGPTTextSync()
