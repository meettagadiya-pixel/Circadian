from fastapi import APIRouter

from app.api.circadian_timeline import (
    circadian_timeline
)

from app.api.behavior_timeline import (
    behavior_timeline
)

router = APIRouter()


@router.get("/combined-timeline")
def combined_timeline(
    user_id: str
):

    circadian = (
        circadian_timeline(
            user_id=user_id
        )
    )

    behavior = (
        behavior_timeline(
            user_id=user_id
        )
    )

    circadian_items = []

    for item in circadian.get(
        "timeline",
        []
    ):

        circadian_items.append({

            "type":
                "circadian",

            "timestamp":
                item.get(
                    "sleep_midpoint"
                ),

            "data":
                item
        })

    behavior_items = []

    for item in behavior.get(
        "timeline",
        []
    ):

        behavior_items.append({

            "type":
                "behavior",

            "timestamp":
                item.get(
                    "timestamp"
                ),

            "data":
                item
        })

    combined = (
        circadian_items
        +
        behavior_items
    )

    combined.sort(
        key=lambda x: x[
            "timestamp"
        ],
        reverse=True
    )

    return {

        "status":
            "success",

        "user_id":
            user_id,

        "count":
            len(
                combined
            ),

        "timeline":
            combined
    }