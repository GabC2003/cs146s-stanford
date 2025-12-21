from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ActionItemBase(BaseModel):
    text: str
    done: bool = False


class ActionItemCreate(ActionItemBase):
    note_id: Optional[int] = None


class ActionItem(ActionItemBase):
    id: int
    note_id: Optional[int]
    created_at: str

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: str
    action_items: List[ActionItem] = []

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ActionItemSummary(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemSummary]


class DoneRequest(BaseModel):
    done: bool = True
