from google.genai import Client, types
from app.core.config import settings
import traceback

class LLMServiceError(Exception):
    pass


class LLMService:
    def __init__(self):
        self.client = Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model
        self.config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024,
        )

    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.config,
            )
        except Exception as e:
            traceback.print_exc()
            raise LLMServiceError(
                "Failed to communicate with Gemini."
            ) from e

        if not response.text:
            raise LLMServiceError(
                "Gemini returned an empty response."
            )

        return response.text