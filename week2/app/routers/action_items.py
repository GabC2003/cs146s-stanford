from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import Connection

from .. import db, schemas
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=schemas.ExtractResponse)
def extract(
    payload: schemas.ExtractRequest, 
    database: Connection = Depends(db.get_db)
) -> schemas.ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note = db.insert_note(database, text)
        note_id = note.id

    # Try heuristic extraction first
    items = extract_action_items(text)
    
    # Fallback to LLM if no items found by heuristics
    if not items:
        items = extract_action_items_llm(text)
        
    summaries = db.insert_action_items(database, items, note_id=note_id)
    return schemas.ExtractResponse(note_id=note_id, items=summaries)


@router.post("/extract-llm", response_model=schemas.ExtractResponse)
def extract_llm(
    payload: schemas.ExtractRequest, 
    database: Connection = Depends(db.get_db)
) -> schemas.ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note = db.insert_note(database, text)
        note_id = note.id

    # Use LLM directly
    items = extract_action_items_llm(text)
        
    summaries = db.insert_action_items(database, items, note_id=note_id)
    return schemas.ExtractResponse(note_id=note_id, items=summaries)


@router.get("", response_model=List[schemas.ActionItem])
def list_all(
    note_id: Optional[int] = None, 
    database: Connection = Depends(db.get_db)
) -> List[schemas.ActionItem]:
    return db.list_action_items(database, note_id=note_id)


@router.post("/{action_item_id}/done")
def mark_done(
    action_item_id: int, 
    payload: schemas.DoneRequest,
    database: Connection = Depends(db.get_db)
) -> dict:
    updated = db.mark_action_item_done(database, action_item_id, payload.done)
    if not updated:
        raise HTTPException(status_code=404, detail="action item not found")
    return {"id": action_item_id, "done": payload.done}


