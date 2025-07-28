from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel, OpenAIResponsesModel
from pydantic_ai.messages import ModelMessage
import os

def get_openai_model(model_name: str) -> OpenAIModel:    
    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return OpenAIResponsesModel(
        model_name,
        provider=provider,
    )

def get_thinking_parts(messages: list[ModelMessage]) -> str:
    thinking_parts: list[str] = []
    for message in messages:
        thinking_parts.extend([part.content for part in message.parts if part.part_kind == "thinking"])
    return "\n".join(thinking_parts)