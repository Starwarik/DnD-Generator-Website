from abc import ABC, abstractmethod
from base64 import b64decode

from app.image.schemas import ImageContainer

from .config import generation_setting

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

import re


class ImageGeneration(ABC):
    @abstractmethod
    def generate_image(self, system_prompt, user_prompt) -> ImageContainer:
        pass


class GigaChatImage(ImageGeneration):
    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.model = self.model.bind_tools(tools=[], tool_choice="auto")

    def generate_image(
        self, system_prompt: str | None, user_prompt: str | None
    ) -> ImageContainer:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(system_prompt))
        if user_prompt:
            messages.append(HumanMessage(user_prompt))
        response = self.model.invoke(messages)
        image_uuid = re.search(r'img src="(.+?)"', response.content).group(1)
        image = self.model.get_file(image_uuid).content
        image = b64decode(image)
        image = ImageContainer(content=image, media_type="image/png")
        return image

image_model = GigaChatImage()