from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from notes import crud, schemas


router = APIRouter()


@router.get("/notes/", response_model=list[schemas.Note])
async def read_notes(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_notes(db=db)


@router.post("/notes/", response_model=schemas.Note)
async def create_note(
    note: schemas.NoteCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    existing_note = await crud.get_note_by_text(db=db, note_text=note.text)
    if existing_note:
        raise HTTPException(status_code=400, detail="Note with this text already exists")

    return await crud.create_note(db=db, note=note)


@router.post("/notes/{note_id}/complete/", response_model=schemas.Note)
async def complete_note(
    note_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    note = await crud.get_note_by_id(db=db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note = await crud.complete_note(db=db, note_id=note_id)

    return note
