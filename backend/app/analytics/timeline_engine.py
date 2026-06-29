import pandas as pd


def build_health_timeline(
    snapshot_rows
):

    if not snapshot_rows:
        return []

    df = pd.DataFrame(snapshot_rows)

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    df = df.sort_values("created_at")

    timeline = []

    for _, row in df.iterrows():

        snapshot_data = row[
            "snapshot_data"
        ]

        risk = snapshot_data.get(
            "risk_analysis",
            {}
        )

        recovery = snapshot_data.get(
            "recovery_protocol",
            {}
        )

        timeline.append({

            "timestamp":
                row["created_at"].isoformat(),

            "fatigue_prediction":
                row.get(
                    "fatigue_prediction"
                ),

            "risk_state":
                risk.get(
                    "risk_state"
                ),

            "risk_score":
                risk.get(
                    "risk_score"
                ),

            "recovery_focus":
                recovery.get(
                    "recovery_focus"
                ),

            "avg_hrv":
                row.get("avg_hrv"),

            "avg_glucose":
                row.get("avg_glucose")
        })

    return timeline