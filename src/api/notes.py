from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, List, Optional
from sqlalchemy import select, update, or_, and_, asc, desc
from sqlalchemy.dialects.postgresql import array
from fastapi import Path

from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.schemas.notes import NoteSchema, NotePutSchema, NoteGetSchema
from src.models.notes import NoteModel

from src.core.security import get_current_user_id

router = APIRouter()

@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database setup completed"}

@router.post("/notes/add", response_model=NoteSchema)
async def add_note(
    note: Annotated[NoteSchema, Depends()],  
    session: SessionDep) -> NoteModel:
    
    new_note = NoteModel(
        user_id=note.user_id,
        title=note.title,
        tags=note.tags,
        text_notes=note.text_notes
    )
    session.add(new_note)
    await session.commit()
    
    return new_note

@router.put("/notes/edit/{note_id}", response_model=NoteSchema)
async def edit_note(
    note_id: Annotated[int, Path(..., title="Здесь указывается id заметки", ge= 1)],
    note_update: Annotated[NotePutSchema, Depends()],  
    session: SessionDep,
    current_user_id: str = Depends(get_current_user_id)) -> NoteModel:
    
    check = await session.execute(
        select(NoteModel).where(NoteModel.id == note_id, NoteModel.user_id == current_user_id)
    )
    note = check.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена или нет доступа")
    
    update_data = note_update.model_dump(exclude_unset=True)
    if not update_data:
        return note
    
    
    query = (
        update(NoteModel)
        .where(NoteModel.id == note_id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
        )
    
    result = await session.execute(query)
    await session.commit()
    
    updated_note = result.scalar_one()
    return updated_note

@router.get("/notes", response_model=List[NoteGetSchema])
async def notes(
    session: SessionDep,
    #sort_by: str = "created_at", #title
    #order: str = "desc", #asc
    #tags: list[str] | None = None,
    #statuses: list[str] | None = None,
    
    sort_by: str = Query("created_at"), #title
    order: str = Query("desc"), #asc
    tags: list[str] = Query(None),
    statuses: list[str] = Query(None),
    
):

    filters = []

    if statuses:
        filters.append(or_(*[NoteModel.status == s for s in statuses]))

    if tags:
        filters.append(NoteModel.tags.op('&&')(array(tags)))

    query = select(NoteModel)
    
    if filters:
        query = query.where(and_(*filters))

    match sort_by:
        case "created_at":
            sort_col = NoteModel.created_at
        case "title":
            sort_col = NoteModel.title
        case _:
            sort_col = NoteModel.created_at
            
    match order:
        case "asc":
            query = query.order_by(asc(sort_col))
        case "desc":
            query = query.order_by(desc(sort_col))
        case _:
            query = query.order_by(desc(sort_col))

    result = await session.execute(query)
    notes = result.scalars().all()
    return notes

@router.get("/notes/{note_id}", response_model=NoteGetSchema)
async def note(
    note_id: Annotated[int, Path(..., title="Здесь указывается id заметки", ge= 1)], 
    session: SessionDep) -> NoteModel:
    
    query = select(NoteModel).where(NoteModel.id == note_id)
    result = await session.execute(query)
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note

