from typing import Dict, Any, Optional
from anthropic import Anthropic
from functools import lru_cache
from app.config import settings


class AIService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    async def generate_details(
        self,
        entity_id: int,
        name: str,
        description: Optional[str] = None,
        existing_attributes: Optional[Dict[str, Any]] = None,
        generation_template: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate details for an entity using AI"""

        # Build context from existing data
        context = f"""
Entity Name: {name}
Description: {description if description else 'Not provided'}
Current Attributes: {existing_attributes if existing_attributes else 'None'}
"""

        # Use generation template if provided, or default prompt
        system_prompt = (
            generation_template.get("system_prompt")
            if generation_template
            else """
Generate detailed information for this entity.
Include relevant attributes based on the entity description.
Return the response as a JSON object with appropriate fields.
"""
        )

        # Make API call to Claude
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            response_format={"type": "json_object"},
        )

        try:
            return response.content[0].text
        except Exception as e:
            raise ValueError(f"Failed to parse AI response: {e}")


@lru_cache()
def get_ai_service() -> AIService:
    """Get a cached instance of AIService"""
    return AIService(api_key=settings.ANTHROPIC_API_KEY)
