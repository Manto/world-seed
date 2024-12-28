import json
from dataclasses import dataclass
from typing import Dict, Any, get_type_hints
from typing_extensions import TypedDict
from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIModel
import logfire
from app.config import settings

WORLD_SETTING = """
In the year 2055, humanity stands at a crossroads. The world we once knew has been reshaped by the relentless march of climate change and technological progress. Coastal cities are threatened by frequent floods exacerbated by rising seas, their former inhabitants now unwelcome wanderers in a world grown hostile to the displaced. Europe shivers under an unprecedented deep freeze, while tropical regions are battered by near-constant storms.

The promise of artificial intelligence, once heralded as our salvation, has proven a double-edged sword. Robots and automation have revolutionized industry and daily life, but at a steep environmental cost. The pursuit of ever-more-powerful AI has accelerated climate change, even as it fails to achieve the long-sought goal of artificial general intelligence.

In this brave new world, productivity soars while birthrates plummet. An aging population finds itself increasingly obsolete, retreating into virtual realities and AI companionship. The gap between the tech-savvy elite and those left behind widens daily. Despite unprecedented technological marvels, famine and disease still plague many corners of the globe.

Humanity finds itself paralyzed, caught between complacency and fear. Some cling desperately to the familiar, while others lose themselves in digital escapes. Tensions simmer as nations close their borders to climate refugees, sparking conflicts and humanitarian crises. Yet beneath the surface, a deeper tension builds – a growing realization that something must change. In this world of environmental chaos and technological wonder, a few dare to ask: can we reclaim our humanity and forge a new path forward? Or are we doomed to be swept away by the very forces we've unleashed?
"""


@dataclass
class AIServiceContext:
    pass


class CharacterStruct(TypedDict, total=False):
    name: str
    profession: str
    background: str
    personality: str
    motivation: str
    hopes: str
    fears: str
    appearance: str


class LocationStruct(TypedDict, total=False):
    name: str
    type: str
    description: str
    purpose: str


class WorldEventStruct(TypedDict, total=False):
    name: str
    when: str
    description: str
    background: str
    outcome: str


TYPE_PROMPTS = {
    "character": {
        "struct": CharacterStruct,
        "agent": Agent(
            deps_type=AIServiceContext,
            result_type=CharacterStruct,
            system_prompt="You are an award winning novel writer. You will be generating compelling ideas for world building."
            "Generate ideas and description for a character using the information provided.",
        ),
    },
    "location": {
        "struct": LocationStruct,
        "agent": Agent(
            deps_type=AIServiceContext,
            result_type=CharacterStruct,
            system_prompt="You are an award winning novel writer. You will be generating compelling ideas for world building."
            "Generate ideas and description for a location using the information provided.",
        ),
    },
    "world_event": {
        "struct": WorldEventStruct,
        "agent": Agent(
            deps_type=AIServiceContext,
            result_type=WorldEventStruct,
            system_prompt="You are an award winning novel writer. You will be generating compelling ideas for world building. "
            "Generate ideas and description for a significant event in the world using the information provided.",
        ),
    },
}

generic_agent = Agent(
    deps_type=AIServiceContext,
    result_type=str,
    system_prompt="You are an award winning novel writer. You will be generating compelling ideas for world building. "
    "Generate ideas and description using the information provided.",
)


def get_model() -> str | Model:
    if settings.USE_LOCAL_MODEL:
        # For running a local OpenAI compatible inference server
        return OpenAIModel(
            settings.AI_MODEL,
            base_url="http://localhost:1234/v1",
        )
    else:
        return settings.AI_MODEL


async def generate_entity_field(
    entity_type: str,
    entity_data: Dict,
    field: str,
    prompt: str,
    append_system_prompt: str = None,
) -> str:

    # Take entity_data, remove fields where value is None and return the result as a new dictionary
    cleaned_entity_data = {k: v for k, v in entity_data.items() if v is not None}

    context = f"""
For the {entity_type} described below, come up with ideas for their {field} using the following information.
Give me just the idea, do not preface what you are writing or give me any title or heading.

World setting:
{WORLD_SETTING}

Existing information with this {entity_type}:
{json.dumps(cleaned_entity_data, indent=2)}

Context and braindump on this {entity_type}:
{prompt}
"""

    try:
        result = await generic_agent.run(
            context,
            model=get_model(),
            model_settings={"temperature": 0.8},
            deps=append_system_prompt,
        )
        return result.data
    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {e}")


async def generate_details_by_field(
    entity_type: str,
    entity_data: Dict,
    prompt: str,
    append_system_prompt: str = None,
) -> Dict[str, Any]:
    """For LLM that does not support structured data, we will generate details field by field"""

    # Loop through entity_data and compare against the structure in TYPE_PROMPTS that matches the given entity_type
    # for each field that is None or missing, generate value using generate_entity_field(), and then return
    # the updated entity_data dictionary.
    if entity_type not in TYPE_PROMPTS:
        raise Exception(f"Entity type {entity_type} not supported")

    for field in get_type_hints(TYPE_PROMPTS[entity_type]["struct"]).keys():
        if field not in entity_data or entity_data[field] is None:
            entity_data[field] = await generate_entity_field(
                entity_type=entity_type,
                entity_data=entity_data,
                field=field,
                prompt=prompt,
                append_system_prompt=append_system_prompt,
            )
    return entity_data


async def generate_details(
    entity_type: str,
    entity_data: Dict,
    prompt: str,
    append_system_prompt: str = None,
) -> Dict[str, Any]:

    context = f"""
Return the result in specified JSON format.

World setting:
{WORLD_SETTING}

Start with this {entity_type} data:
{json.dumps(entity_data, indent=2)}

Guidance for filling out {entity_type} details:
{prompt}
"""

    try:
        agent = TYPE_PROMPTS.get(entity_type).get("agent")
        result = await agent.run(
            context,
            model=get_model(),
            model_settings={"temperature": 0.8},
            deps=append_system_prompt,
        )
        return result.data
    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {e}")


if __name__ == "__main__":
    import asyncio
    from pprint import pprint

    result = asyncio.run(
        generate_details(
            entity_type="character",
            entity_data={"name": "Jason Hikaru"},
            prompt="A hard-boiled detective who is down on his luck, but has a secret that could change everything.",
        )
    )
    pprint(result)
