from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.anomaly_engine import (
    detect_physiological_anomalies
)

from app.analytics.risk_engine import (
    calculate_risk_state
)

router = APIRouter()


@router.get("/risk/{user_id}")
def get_risk_state(user_id: str):

    # -------------------------
    # Snapshot history
    # -------------------------

    snapshot_resp = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .limit(30)
        .execute()
    )

    snapshots = snapshot_resp.data

    anomaly_analysis = (
        detect_physiological_anomalies(
            snapshots
        )
    )

    latest = snapshots[-1]

    snapshot_data = latest[
        "snapshot_data"
    ]

    digital_twin = snapshot_data[
        "digital_twin"
    ]

    metabolic = digital_twin[
        "metabolic_analysis"
    ]

    misalignment = digital_twin[
        "misalignment_analysis"
    ]

    fatigue_prediction = latest[
        "fatigue_prediction"
    ]

    risk = calculate_risk_state(
        anomaly_analysis=anomaly_analysis,
        fatigue_prediction=fatigue_prediction,
        misalignment_hours=misalignment[
            "misalignment_hours"
        ],
        glucose_variability=metabolic[
            "glucose_variability"
        ]
    )

    return {
        "user_id": user_id,
        "risk_analysis": risk,
        "anomaly_analysis": anomaly_analysis
    }