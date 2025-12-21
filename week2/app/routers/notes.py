from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import Connection

from .. import db, schemas


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=schemas.Note)
def create_note(
    payload: schemas.NoteCreate, 
    database: Connection = Depends(db.get_db)
) -> schemas.Note:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    return db.insert_note(database, content)


@router.get("", response_model=List[schemas.Note])
def list_notes(database: Connection = Depends(db.get_db)) -> List[schemas.Note]:
    return db.list_notes(database)


@router.get("/{note_id}", response_model=schemas.Note)
def get_single_note(
    note_id: int, 
    database: Connection = Depends(db.get_db)
) -> schemas.Note:
    note = db.get_note(database, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    return note


