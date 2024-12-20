from app.generation.generation_text_service import generate_text_with_tries
from app.generation.text_models import text_generation_model
from app.adventure.schemas import *
from app.generation.schemas import *
from app.generation.instructions import *
import asyncio


async def main():
    adventure_info = AdventureInfo(
        name="Храм Грача",
        location="Храм Грача",
        setting="Фентези",
        playerNum=2,
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        NPCsInstruction(),
        QuestsInstruction(),
    ]

    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, text_generation_model
    )
    print(adventure_info, spented_tokens_counts)


asyncio.run(main())
