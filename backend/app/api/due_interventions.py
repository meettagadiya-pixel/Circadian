from datetime import datetime, timezone

from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


def parse_datetime_safe(
    value
):

    dt = datetime.fromisoformat(
        value.replace(
            "Z",
            "+00:00"
        )
    )

    if dt.tzinfo is None:

        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return dt


@router.get("/due-interventions")
def due_interventions(
    user_id: str
):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:

        return {
            "status": "no_snapshot",
            "user_id": user_id,
            "due_interventions": []
        }

    snapshot = response.data[0]

    snapshot_data = snapshot.get(
        "snapshot_data",
        {}
    )

    scheduled = snapshot_data.get(
        "scheduled_interventions",
        []
    )

    now = datetime.now(
        timezone.utc
    )

    due = []

    for item in scheduled:

        scheduled_time = item.get(
            "scheduled_time"
        )

        if not scheduled_time:
            continue

        scheduled_dt = parse_datetime_safe(
            scheduled_time
        )

        age_hours = (
            now - scheduled_dt
        ).total_seconds() / 3600

        if (
            scheduled_dt <= now
            and
            age_hours <= 24
        ):

            due.append(
                item
            )

    return {
        "status": "success",
        "user_id": user_id,
        "checked_at": now.isoformat(),
        "due_count": len(due),
        "due_interventions": due
    }