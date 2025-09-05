from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from ..llm.router import router as llm_router

api = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class CompletionRequest(BaseModel):
    provider: str = Field(..., description="Provider name: openai, anthropic, gemini")
    model: str = Field(..., description="Model name or ID")
    messages: List[Message]


@api.post("/llm/complete")
async def complete(req: CompletionRequest):
    try:
        message = await llm_router.complete(
            provider=req.provider.lower(),
            model=req.model,
            messages=[m.dict() for m in req.messages],
        )
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

