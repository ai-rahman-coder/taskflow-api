from app.schemas.note_schema import NoteCreate, NoteReplace, NoteResponse, NoteUpdate
from datetime import datetime

# Temporary in-memory storage for notes
notes_db = []
note_id_counter = 1

def create_note(note: NoteCreate, user_id) -> NoteResponse:
    global note_id_counter

    new_note = NoteResponse(
        id = note_id_counter,
        title = note.title,
        content = note.content,
        owner_id = user_id,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_archived = False
    )

    notes_db.append(new_note)
    note_id_counter += 1

    return new_note

def get_notes() -> list[NoteResponse]:
    return notes_db

def get_note_by_id(note_id: int) -> NoteResponse | None:
    for note in notes_db:
        if note.id == note_id:
            return note
    return None


def replace_note(existing_note, replace_note: NoteReplace) -> NoteResponse | None:
    existing_note.title = replace_note.title
    existing_note.content = replace_note.content
    existing_note.updated_at = datetime.now()
    return existing_note


def update_note(note_id: int, updated_note: NoteUpdate) -> NoteResponse | None:
    for note in notes_db:
        if note.id == note_id:
            if updated_note.title is not None:
                note.title = updated_note.title
            if updated_note.content is not None:
                note.content = updated_note.content
            if updated_note.is_archived is not None:
                note.is_archived = updated_note.is_archived
            note.updated_at = datetime.now()
            return note
    return None


def archive_note(note) -> NoteResponse | None:
    if note.is_archived:
        return None
    note.is_archived = True
    note.updated_at = datetime.now()
    return note

def unarchive_note(note_id: int) -> NoteResponse | None:
    for note in notes_db:
        if note.id == note_id:
            if not note.is_archived:
                return None
            note.is_archived = False
            note.updated_at = datetime.now()
            return note
    return None

def delete_note(note_id: int) -> bool:
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            del notes_db[i]
            return True
    return False