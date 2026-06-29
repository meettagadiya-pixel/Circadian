import random
from datetime import datetime


def generate_mock_physiology(
    user_id
):

    return {
        "user_id": user_id,

        "timestamp":
            datetime.utcnow().isoformat(),

        "core_body_temp":
            round(
                random.uniform(
                    36.1,
                    37.2
                ),
                2
            ),

        "hrv":
            round(
                random.uniform(
                    35,
                    75
                ),
                2
            ),

        "resting_heart_rate":
            round(
                random.uniform(
                    55,
                    80
                ),
                2
            )
    }