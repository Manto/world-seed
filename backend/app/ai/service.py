from typing import Dict, Any, Optional
from anthropic import Anthropic
import json


class AIService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

        # Templates for different entity types
        self.templates = {
            "Character": {
                "system_prompt": """
                Generate detailed character information for a world-building project.
                Include the following aspects:
                - profession: Their current occupation and role
                - desires: Main motivations and goals
                - appearance: Detailed physical description
                - personality: Key character traits
                
                Return the response as a JSON object with these fields.
                """,
            },
            "Area": {
                "system_prompt": """
                Generate detailed area information for a world-building project.
                Include the following aspects:
                - climate: Weather patterns and environmental conditions
                - geography: Physical features and landmarks
                - culture: Predominant customs and social structures
                - resources: Notable natural or manufactured resources
                
                Return the response as a JSON object with these fields.
                """,
            },
            "Location": {
                "system_prompt": """
                Generate detailed location information for a world-building project.
                Include the following aspects:
                - purpose: Main function or use of the location
                - atmosphere: Overall mood and ambiance
                - notable_features: Unique or important characteristics
                - history: Brief background of the location
                
                Return the response as a JSON object with these fields.
                """,
            },
        }

    async def generate_details(
        self,
        entity_type: str,
        name: str,
        description: Optional[str] = None,
        existing_attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        template = self.templates.get(entity_type)
        if not template:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        # Build the prompt
        context = f"Name: {name}\n"
        if description:
            context += f"Initial Description: {description}\n"
        if existing_attributes:
            context += (
                f"Existing Information: {json.dumps(existing_attributes, indent=2)}\n"
            )

        messages = [
            {"role": "system", "content": template["system_prompt"]},
            {
                "role": "user",
                "content": f"Generate details for this {entity_type.lower()}:\n{context}",
            },
        ]

        # Make API call to Claude
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=messages,
            response_format={"type": "json_object"},
        )

        try:
            generated_content = json.loads(response.content[0].text)
            return generated_content
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI response as JSON")

    async def generate_relationships(
        self, entity_type: str, entity_name: str, related_entities: Dict[str, list]
    ) -> Dict[str, Any]:
        """Generate suggestions for relationships with other entities"""

        context = f"""
        Entity: {entity_name} (Type: {entity_type})
        Existing related entities:
        {json.dumps(related_entities, indent=2)}
        
        Suggest potential relationships or connections with the listed entities.
        Consider:
        - Hierarchical relationships (contains/contained by)
        - Social relationships (for characters)
        - Geographic relationships (for areas/locations)
        - Historical connections
        
        Return the response as a JSON object with suggested relationships.
        """

        messages = [
            {
                "role": "system",
                "content": "You are a world-building assistant. Generate creative but logical relationships between entities.",
            },
            {"role": "user", "content": context},
        ]

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=messages,
            response_format={"type": "json_object"},
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI response as JSON")


# Usage example
# ai_service = AIService(api_key="your-anthropic-api-key")
# details = await ai_service.generate_details("Character", "Eldrin the Wise",
#                                           "An ancient sage living in the mountain temple")
