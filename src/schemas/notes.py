from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlalchemy import String, ARRAY

class NoteSchema(BaseModel):
    user_id: int
    title: str
    tags: list[str] = []
    text_notes: str | None = None
    audio_path: str | None = None
    transcript: str | None = None
    summary: str | None = None
    status: str = "pending_transcription"

class NotePutSchema(BaseModel):
    user_id: int | None = None
    title: str | None  = None
    tags: list[str] | None = None
    text_notes: str | None = None
    audio_path: str | None = None
    transcript: str | None = None
    summary: str | None = None
    status: str | None = None

# "pending_transcription" | "pending_summarization" | "completed" | "failed" = "pending_transcription"
class NoteGetSchema(NoteSchema):
    id: int
    created_at: datetime
    updated_at: datetime