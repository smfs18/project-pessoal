from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TriageSession(BaseModel):
    session_id: str  # ID único da sessão/usuário
    messages: List[Message] = []
    triage_summary: str | None = None
    is_emergency: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)