from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class BehaviorLog(BaseModel):
    user_id: str
    event_type: str
    notes: str
    timestamp: Optional[str] = None  # ISO string, if None uses now


@router.post("/log-behavior")
def log_behavior(
    payload: BehaviorLog
):
    # Use provided timestamp or current UTC time
    if payload.timestamp:
        try:
            ts = payload.timestamp
        except Exception:
            ts = datetime.now(timezone.utc).isoformat()
    else:
        ts = datetime.now(timezone.utc).isoformat()

    record = {
        "user_id": payload.user_id,
        "timestamp": ts,
        "event_type": payload.event_type,
        "notes": payload.notes
    }

    response = (
        supabase
        .table("behavioral_logs")
        .insert(record)
        .execute()
    )

    return {
        "status": "logged",
        "event_type": payload.event_type,
        "timestamp": ts,
        "data": response.data
    }


@router.get("/behavior-logs")
def get_behavior_logs(
    user_id: str,
    limit: int = 20
):
    """Return recent behavioral logs for a user."""

    response = (
        supabase
        .table("behavioral_logs")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )

    return {
        "status": "success",
        "user_id": user_id,
        "logs": response.data or []
    }