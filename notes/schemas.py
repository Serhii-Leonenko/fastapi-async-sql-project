from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    text: str
    completed: bool | None = False


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
