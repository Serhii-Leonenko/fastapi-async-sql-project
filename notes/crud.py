from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from notes import models, schemas


async def get_all_notes(db: AsyncSession) ->  list[models.Note]:
    notes = await db.scalars(select(models.Note))

    return notes.all()


async def get_note_by_text(db: AsyncSession, note_text: str) -> models.Note | None:
    return await db.scalar(select(models.Note).where(models.Note.text == note_text))


async def create_note(db: AsyncSession, note: schemas.NoteCreate) -> models.Note:
    note = models.Note(
        text=note.text,
        completed=note.completed,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


async def get_note_by_id(db: AsyncSession, note_id: int) -> models.Note | None:
    return await db.scalar(select(models.Note).where(models.Note.id == note_id))


async def complete_note(db: AsyncSession, note_id: int) -> models.Note:
    note = await get_note_by_id(db=db, note_id=note_id)
    note.completed = True
    await db.commit()
    await db.refresh(note)

    return note
