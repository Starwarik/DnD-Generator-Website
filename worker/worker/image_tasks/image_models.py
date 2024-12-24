from abc import ABC, abstractmethod
from base64 import b64decode

from worker.database.schemas import ImageContainer, SpentedTokensCounts

from worker.config import generation_setting

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

import re


class ImageGeneration(ABC):
    """
    Абстрактный класс модели для генерации картинок.
    """

    @abstractmethod
    def generate_image(
        self, system_prompt: str | None, user_prompt: str | None
    ) -> tuple[ImageContainer, SpentedTokensCounts]:
        """
        По заданному промпту генерирует картинку.
        :param system_prompt: Системный промпт. Может не указываться
        :param user_prompt: Системный промпт. Может не указываться
        """
        raise NotImplementedError()


class GigaChatImage(ImageGeneration):
    """
    Класс для генерации модели с использованием Гигачата.
    """

    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.model = self.model.bind_tools(tools=[], tool_choice="auto")

    def generate_image(
        self, system_prompt: str | None, user_prompt: str | None
    ) -> tuple[ImageContainer, SpentedTokensCounts]:
        """
        По заданному промпту генерирует картинку.
        :param system_prompt: Системный промпт. Может не указываться
        :param user_prompt: Системный промпт. Может не указываться
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(system_prompt))
        if user_prompt:
            messages.append(HumanMessage(user_prompt))
        response = self.model.invoke(messages)

        image_uuid = re.search(r'img src="(.+?)"', response.content).group(1)
        image = self.model.get_file(image_uuid).content
        image = b64decode(image)
        image = ImageContainer(content=image, media_type="image/jpeg")

        spented_tokens = SpentedTokensCounts(
            image_generated=1,
            gigachat_assistant_token_count=response.response_metadata[
                "token_usage"
            ].completion_tokens,
            gigachat_prompt_token_count=response.response_metadata[
                "token_usage"
            ].prompt_tokens,
        )
        return (image, spented_tokens)


image_model = GigaChatImage()
