import sqlite3
from typing import Generator, List, Optional
from .config import settings
from . import schemas


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Dependency for getting a database connection."""
    ensure_data_directory_exists()
    connection = sqlite3.connect(settings.DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def ensure_data_directory_exists() -> None:
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    ensure_data_directory_exists()
    with sqlite3.connect(settings.DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def insert_note(db: sqlite3.Connection, content: str) -> schemas.Note:
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    db.commit()
    note_id = cursor.lastrowid
    return get_note(db, note_id)


def list_notes(db: sqlite3.Connection) -> List[schemas.Note]:
    cursor = db.cursor()
    cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
    rows = cursor.fetchall()
    return [schemas.Note(
        id=row["id"], 
        content=row["content"], 
        created_at=row["created_at"],
        action_items=list_action_items(db, note_id=row["id"])
    ) for row in rows]


def get_note(db: sqlite3.Connection, note_id: int) -> Optional[schemas.Note]:
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, content, created_at FROM notes WHERE id = ?",
        (note_id,),
    )
    row = cursor.fetchone()
    if not row:
        return None
    
    return schemas.Note(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"],
        action_items=list_action_items(db, note_id=note_id)
    )


def insert_action_items(db: sqlite3.Connection, items: List[str], note_id: Optional[int] = None) -> List[schemas.ActionItemSummary]:
    cursor = db.cursor()
    summaries: List[schemas.ActionItemSummary] = []
    for item in items:
        cursor.execute(
            "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
            (note_id, item),
        )
        summaries.append(schemas.ActionItemSummary(id=cursor.lastrowid, text=item))
    db.commit()
    return summaries


def list_action_items(db: sqlite3.Connection, note_id: Optional[int] = None) -> List[schemas.ActionItem]:
    cursor = db.cursor()
    if note_id is None:
        cursor.execute(
            "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
        )
    else:
        cursor.execute(
            "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
            (note_id,),
        )
    rows = cursor.fetchall()
    return [schemas.ActionItem(
        id=row["id"],
        note_id=row["note_id"],
        text=row["text"],
        done=bool(row["done"]),
        created_at=row["created_at"]
    ) for row in rows]


def mark_action_item_done(db: sqlite3.Connection, action_item_id: int, done: bool) -> bool:
    cursor = db.cursor()
    cursor.execute(
        "UPDATE action_items SET done = ? WHERE id = ?",
        (1 if done else 0, action_item_id),
    )
    db.commit()
    return cursor.rowcount > 0


