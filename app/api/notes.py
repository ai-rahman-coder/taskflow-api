from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from app.services.note_service import archive_note, create_note, get_note_by_id, get_notes, replace_note, unarchive_note, update_note, delete_note
from app.schemas.note_schema import NoteCreate, NoteListResponse, NoteReplace, NoteResponse, NoteUpdate
from app.core.auth import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=NoteResponse)
def create_note_api(note: NoteCreate, current_user = Depends(get_current_user)):
    return create_note(note, current_user["id"])

@router.get("", response_model=NoteListResponse)
def get_notes_api(
    title: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    current_user = Depends(get_current_user)
    ):
    notes = get_notes()

    if current_user["role"] != "admin":
        notes = [note for note in notes if note.owner_id == current_user["id"]]

    if title:
        notes = [note for note in notes if title.lower() in note.title.lower()]

    total = len(notes)

    notes = notes[skip: skip + limit]
    return {"notes": notes, "total": total}


@router.put("/{note_id}", response_model=NoteResponse)
def replace_note_api(note_id: int, note: NoteReplace, current_user = Depends(get_current_user)):
    existing_note = get_note_by_id(note_id)
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user["role"] != "admin" and existing_note.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this note")

    replace = replace_note(existing_note, note)
    if not replace:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return replace


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note_api(note_id: int, note: NoteUpdate, current_user = Depends(get_current_user)):
    note = get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user["role"] != "admin" and note.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this note")
    
    updated = update_note(note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.patch("/{note_id}/archive")
def archive_note_api(note_id: int, current_user = Depends(get_current_user)):
    existing_note = get_note_by_id(note_id)
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user["role"] != "admin" and existing_note.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this note")
    
    note = archive_note(existing_note)
    if not note:
        raise HTTPException(status_code=404, detail="Note already archived")
    return {"message": "Note archived successfully"}

@router.patch("/{note_id}/unarchive")
def unarchive_note_api(note_id: int, current_user = Depends(get_current_user)):
    existing_note = get_note_by_id(note_id)
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user["role"] != "admin" and existing_note.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this note")
    
    note = unarchive_note(existing_note)
    if not note:
        raise HTTPException(status_code=404, detail="Note already unarchived")
    return {"message": "Note unarchived successfully"}


@router.delete("/{note_id}")
def delete_note_api(note_id: int, current_user = Depends(get_current_user)):
    note = get_note_by_id(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if current_user["role"] != "admin" and note.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    delete_note(note_id)

    return {"message": "Note deleted successfully"}