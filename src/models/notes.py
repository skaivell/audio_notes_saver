from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, ARRAY, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from src.database import Base

class NoteModel(Base):
    __tablename__ = "notes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(default="Новая заметка")
    tags: Mapped[list] = mapped_column(ARRAY(String), default=[])
    text_notes: Mapped[str | None]
    audio_path: Mapped[str | None]
    transcript: Mapped[str | None]
    summary: Mapped[str | None]
    status: Mapped[str] = mapped_column(default="pending_transcription")

#class NoteModel(Base):
#    __tablename__ = "notes"
#    
#    id = Column(Integer, primary_key=True)
#    user_id = Column(String, nullable=False, index=True)
#    title = Column(String, default="Новая заметка")
#    tags = Column(ARRAY[String], default=list)
#    text_notes = Column(Text, nullable=True)
#    audio_path = Column(String)
#    transcript = Column(Text, nullable=True)
#    summary = Column(Text, nullable=True)
#    status = Column(String, default="pending_transcription")
#    created_at = Column(DateTime(timezone=True), server_default=func.now())
#    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#class Note(Base):
#    __tablename__ = "notes"
#    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#    user_id = sa.Column(UUID(as_uuid=True), nullable=False)
#    title = sa.Column(sa.String, nullable=False)
#    tags = sa.Column(ARRAY(sa.String), nullable=True)
#    notes_text = sa.Column(sa.Text, nullable=True)
#    audio_path = sa.Column(sa.String, nullable=False)
#    status = sa.Column(sa.Enum('pending_transcription','pending_summarization','completed','failed', name='note_status'), default='pending_transcription', nullable=False)
#    transcription_text = sa.Column(sa.Text, nullable=True)
#    summary_text = sa.Column(sa.Text, nullable=True)
#    summary_llm_model = sa.Column(sa.String, nullable=True)
#    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
#    updated_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)