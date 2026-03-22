from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: Optional[str] = Field(None, max_length=300)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_archived: bool

class NoteListResponse(BaseModel):
    notes: list[NoteResponse]
    total: int

class NoteReplace(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: Optional[str] = Field(None, max_length=300)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    content: Optional[str] = Field(None, max_length=300)
    is_archived: Optional[bool] = None