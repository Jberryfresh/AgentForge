from fastapi import APIRouter
from ..core.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"name": settings.PROJECT_NAME, "version": settings.VERSION}
