from fastapi import APIRouter

from app.api.due_interventions import (
    due_interventions
)

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get(
    "/notification-preview"
)
def notification_preview(
    user_id: str
):

    response = due_interventions(
        user_id=user_id
    )

    due = response.get(
        "due_interventions",
        []
    )

    delivered_response = (
        supabase
        .table("notification_delivery_log")
        .select("notification_key")
        .eq("user_id", user_id)
        .execute()
    )

    delivered_keys = {
        item["notification_key"]
        for item in delivered_response.data
    }

    notifications = []

    for item in due:

        intervention_type = item.get(
            "type",
            "general"
        )

        message = item.get(
            "message",
            ""
        )

        notification_key = (
            item.get("type", "")
            +
            "|"
            +
            item.get("scheduled_time", "")
            +
            "|"
            +
            message
        )

        if notification_key in delivered_keys:
            continue

        title = "Circadian Guidance"
        emoji = "🧠"

        if intervention_type == (
            "light_exposure"
        ):

            if (
                "after 10 PM" in message
                or
                "Reduce bright" in message
            ):

                title = "Evening Light"
                emoji = "🌙"

            else:

                title = "Morning Light"
                emoji = "🌞"

        elif intervention_type == (
            "sleep_timing"
        ):

            title = "Sleep Timing"
            emoji = "😴"

        elif intervention_type == (
            "sleep_schedule"
        ):

            title = "Sleep Schedule"
            emoji = "🛏️"

        elif intervention_type == (
            "nutrition"
        ):

            title = "Nutrition Timing"
            emoji = "🥗"

        elif intervention_type == (
            "exercise_timing"
        ):

            title = "Exercise Timing"
            emoji = "🏃"

        elif intervention_type == (
            "recovery"
        ):

            title = "Recovery"
            emoji = "🔋"

        notifications.append({

            "title":
                title,

            "emoji":
                emoji,

            "message":
                message,

            "priority":
                item.get(
                    "priority"
                ),

            "scheduled_time":
                item.get(
                    "scheduled_time"
                ),

            "notification_key":
                notification_key,
        })

    return {

        "status":
            "success",

        "user_id":
            user_id,

        "notification_count":
            len(
                notifications
            ),

        "notifications":
            notifications
    }