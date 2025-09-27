from fastapi import APIRouter, Form
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import uuid

router = APIRouter()
def init_db():
    conn = sqlite3.connect("sessions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            start_time TEXT,
            end_time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
class LogoutRequest(BaseModel):
    session_id: str


@router.post("/login")
async def login(name: str = Form(...), email: str = Form(...)):
    session_id = str(uuid.uuid4())
    start_time = datetime.utcnow().isoformat()

    conn = sqlite3.connect("sessions.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (id, name, email, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
        (session_id, name, email, start_time, None),
    )
    conn.commit()
    conn.close()

    return {"session_id": session_id, "start_time": start_time}


@router.post("/logout")
async def logout(request: LogoutRequest):
    end_time = datetime.utcnow().isoformat()

    conn = sqlite3.connect("sessions.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET end_time = ? WHERE id = ?",
        (end_time, request.session_id),
    )
    conn.commit()
    conn.close()

    return {"message": "Session ended", "end_time": end_time}
