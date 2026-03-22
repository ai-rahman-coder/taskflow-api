from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.note_service import archive_note, create_note, get_notes, replace_note, unarchive_note, update_note
from app.schemas.note_schema import NoteCreate, NoteListResponse, NoteReplace, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=NoteResponse)
def create_note_api(note: NoteCreate):
    return create_note(note)

@router.get("", response_model=NoteListResponse)
def get_notes_api(
    title: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
    ):
    notes = get_notes()

    if title:
        notes = [note for note in notes if title.lower() in note.title.lower()]

    total = len(notes)

    notes = notes[skip: skip + limit]
    return {"notes": notes, "total": total}


@router.put("/{note_id}", response_model=NoteResponse)
def replace_note_api(note_id: int, note: NoteReplace):
    replace = replace_note(note_id, note)
    if not replace:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return replace


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note_api(note_id: int, note: NoteUpdate):
    updated = update_note(note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return updated


@router.patch("/{note_id}/archive")
def archive_note_api(note_id: int):
    note = archive_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or already archived")
    
    return {"message": "Note archived successfully"}

@router.patch("/{note_id}/unarchive")
def unarchive_note_api(note_id: int):
    note = unarchive_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or already unarchived")
    
    return {"message": "Note unarchived successfully"}