from abc import ABC, abstractmethod

from .config import generation_setting

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from pydantic import BaseModel


class Image(BaseModel):
    content_b64: str
    media_type: str


class ImageGeneration(ABC):
    @abstractmethod
    def generate_image(self, system_prompt, user_prompt) -> Image:
        pass


class GigaChatImage(ImageGeneration):
    def __init__(self):
        self.model = GigaChat(
            credentials=generation_setting.gigachat_credentials, verify_ssl_certs=False
        )
        self.model.bind_tools(tools=[], tool_choice="auto")

    def generate_image(
        self, system_prompt: str | None, user_prompt: str | None
    ) -> Image:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(system_prompt))
        if user_prompt:
            messages.append(HumanMessage(user_prompt))
        response = self.model(messages)
        image_uuid = response.additional_kwargs.get("image_uuid")
        image = self.model.get_file(image_uuid).content
        image = Image(content=image, media_type="image/png")
        return image
