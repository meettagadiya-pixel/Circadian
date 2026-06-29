from fastapi import APIRouter

from workers.physiology_worker import (
    run_physiology_pipeline
)

router = APIRouter()


@router.post("/junction-webhook")
async def junction_webhook(
    payload: dict
):

    event_type = payload.get(
        "type"
    )

    user_id = payload.get(
        "user_id"
    )

    print(
        f"Webhook received: "
        f"{event_type}"
    )

    print(
        f"User: {user_id}"
    )

    # -------------------------
    # TRIGGER REAL-TIME UPDATE
    # -------------------------

    run_physiology_pipeline()

    return {

        "status":
            "processed",

        "event_type":
            event_type
    }