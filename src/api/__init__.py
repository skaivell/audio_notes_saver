from fastapi import APIRouter

from src.api.notes import router as notes_router

main_router = APIRouter()

main_router.include_router(notes_router, prefix="", tags=["notes"])