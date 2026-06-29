import pandas as pd


def analyze_snapshot_trends(snapshot_rows):

    if not snapshot_rows:
        return None

    df = pd.DataFrame(snapshot_rows)

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    df = df.sort_values("created_at")

    fatigue_trend = (
        df["fatigue_prediction"]
        .astype(float)
        .mean()
    )

    hrv_trend = (
        df["avg_hrv"]
        .astype(float)
        .mean()
    )

    glucose_trend = (
        df["avg_glucose"]
        .astype(float)
        .mean()
    )

    return {
        "average_fatigue_prediction": round(
            fatigue_trend,
            2
        ),

        "average_hrv": round(
            hrv_trend,
            2
        ),

        "average_glucose": round(
            glucose_trend,
            2
        ),

        "snapshot_count": len(df)
    }