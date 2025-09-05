import os
import asyncio
from typing import List, Dict, Any

from openai import AsyncOpenAI
import anthropic
import google.generativeai as genai


class LLMRouter:
    def __init__(self):
        # API keys are optional at init; real calls will fail if unset.
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    async def complete(self, provider: str, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        provider = provider.lower()
        if provider == "openai":
            # OpenAI async chat completion via new client
            response = await self.openai.chat.completions.create(
                model=model,
                messages=messages,
            )
            msg = response.choices[0].message
            return {"role": msg.role, "content": msg.content}
        elif provider == "anthropic":
            content = "".join(m.get("content", "") for m in messages)
            # Anthropics SDK is sync; offload to thread to avoid blocking the loop
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=1024,
            )
            return {"role": "assistant", "content": getattr(response, "content", "")}
        elif provider == "gemini":
            client = genai.GenerativeModel(model)
            chat = client.start_chat(history=messages)
            response = await chat.send_message_async(content=messages[-1]["content"])  # type: ignore[attr-defined]
            # Normalize to a message-like dict
            part = response.candidates[0].content.parts[0]
            # Try to extract text field if present
            text = getattr(part, "text", None) or getattr(part, "raw_text", None) or str(part)
            return {"role": "assistant", "content": text}
        else:
            raise ValueError(f"Unsupported provider: {provider}")


router = LLMRouter()
