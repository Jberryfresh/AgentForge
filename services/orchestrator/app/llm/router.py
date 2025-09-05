import os
from typing import List, Dict, Any

import openai
import anthropic
import google.generativeai as genai


class LLMRouter:
    def __init__(self):
        # API keys are optional at init; real calls will fail if unset.
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    async def complete(self, provider: str, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        provider = provider.lower()
        if provider == "openai":
            # OpenAI async chat completion (compat with >=1.12 legacy style)
            response = await openai.ChatCompletion.acreate(model=model, messages=messages)  # type: ignore[attr-defined]
            return response.choices[0].message
        elif provider == "anthropic":
            content = "".join(m.get("content", "") for m in messages)
            response = await self.anthropic_client.messages.create(  # type: ignore[func-returns-value]
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=1024,
            )
            return {"role": "assistant", "content": response.content}
        elif provider == "gemini":
            client = genai.GenerativeModel(model)
            chat = client.start_chat(history=messages)
            response = await chat.send_message_async(content=messages[-1]["content"])  # type: ignore[attr-defined]
            # Normalize to a message-like dict
            return response.candidates[0].content.parts[0]
        else:
            raise ValueError(f"Unsupported provider: {provider}")


router = LLMRouter()

