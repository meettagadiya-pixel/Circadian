from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


def readiness_label(score):

    if score >= 80:
        return "optimal"
    if score >= 60:
        return "good"
    if score >= 40:
        return "moderate"
    if score >= 20:
        return "low"
    return "very low"


@router.get("/readiness-score")
def readiness_score(user_id: str):

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
            "status": "no_data",
            "user_id": user_id
        }

    snapshot = response.data[0]
    data = snapshot.get("snapshot_data", {})
    misalignment = data.get("misalignment", {})
    adherence = data.get("adherence", {})

    avg_hrv = snapshot.get("avg_hrv", 0) or 0
    fatigue_prediction = snapshot.get("fatigue_prediction", 0) or 0

    # ─────────────────────────────────────────────────────────
    # COMPONENT 1 — HRV SCORE (0-100) — weight 55%
    #
    # Largest single contributor to readiness per:
    # Oura Ring validation study (Koskimäki et al., 2018)
    # Firstbeat Technologies white paper (2014)
    # Heart rate variability reference ranges (Shaffer & Ginsberg, 2017)
    #
    # Reference ranges used (adult, resting, night HRV):
    #   > 60ms  = high autonomic recovery   → score 75-100
    #   40-60ms = good recovery             → score 50-75
    #   20-40ms = reduced recovery          → score 20-50
    #   < 20ms  = low autonomic activity    → score 5-20
    # ─────────────────────────────────────────────────────────

    if avg_hrv >= 60:
        hrv_score = min(100, 75 + (avg_hrv - 60) * 0.5)
    elif avg_hrv >= 40:
        hrv_score = 50 + (avg_hrv - 40) * 1.25
    elif avg_hrv >= 20:
        hrv_score = 20 + (avg_hrv - 20) * 1.5
    else:
        hrv_score = max(5, avg_hrv * 0.75)

    # ─────────────────────────────────────────────────────────
    # COMPONENT 2 — SLEEP QUALITY SCORE (0-100) — weight 28%
    #
    # Combines:
    #   - Circadian consistency (sleep regularity index)
    #   - Fatigue state (HRV-derived, from our transparent formula)
    #
    # Sleep regularity is a strong independent predictor of
    # next-day cognitive performance and recovery.
    # (Phillips et al., 2017 — Scientific Reports)
    #
    # Fatigue 1-5 → converted to 0-100 penalty:
    #   fatigue 1 (low)    → fatigue_score 100
    #   fatigue 5 (severe) → fatigue_score 0
    # ─────────────────────────────────────────────────────────

    consistency_score = misalignment.get("consistency_score", 0) or 0
    consistency_pct = consistency_score * 100

    # Fatigue contribution (inverse — lower fatigue = higher score)
    fatigue_score = max(0, 100 - ((fatigue_prediction - 1) / 4) * 100)

    # Sleep quality = average of consistency and fatigue recovery
    sleep_quality_score = (consistency_pct * 0.5) + (fatigue_score * 0.5)

    # ─────────────────────────────────────────────────────────
    # COMPONENT 3 — BEHAVIOURAL ADHERENCE SCORE (0-100) — weight 17%
    #
    # Reflects how consistently the user follows circadian-aligned
    # behaviours (meal timing, exercise timing, sleep schedule).
    # Lower weight than HRV and sleep because it is more
    # subject to voluntary choice and less directly physiological.
    # (Baron & Reid, 2014 — circadian behavioural interventions)
    # ─────────────────────────────────────────────────────────

    overall_adherence = adherence.get("overall_adherence", 0) or 0
    adherence_score = overall_adherence * 100

    # ─────────────────────────────────────────────────────────
    # FINAL READINESS SCORE
    #
    # Weighted sum — evidence-based allocation:
    #   HRV/autonomic:  55% (strongest physiological signal)
    #   Sleep quality:  28% (consistency + fatigue)
    #   Adherence:      17% (behavioural patterns)
    #
    # Total always sums to 100% — no circular risk penalty.
    # Risk is a separate downstream indicator (Circadian Stress
    # Index) and should not feed back into readiness to avoid
    # circular dependency.
    # ─────────────────────────────────────────────────────────

    readiness = (
        (hrv_score         * 0.55)
        + (sleep_quality_score * 0.28)
        + (adherence_score     * 0.17)
    )

    readiness = max(0, min(100, round(readiness)))

    # ─────────────────────────────────────────────────────────
    # CONTEXTUAL RECOMMENDATION
    # Based on readiness level + primary limiting factor
    # ─────────────────────────────────────────────────────────

    # Identify the weakest driver to give specific advice
    drivers_scored = {
        "hrv":        hrv_score,
        "sleep":      sleep_quality_score,
        "adherence":  adherence_score
    }
    weakest = min(drivers_scored, key=drivers_scored.get)

    recommendations = []

    if readiness < 30:
        if weakest == "hrv":
            recommendations.append(
                "HRV is very low — your autonomic system needs recovery. "
                "Avoid intense exercise, alcohol, and late screens tonight."
            )
        elif weakest == "sleep":
            recommendations.append(
                "Sleep consistency is poor and fatigue is high. "
                "Prioritise a fixed bedtime tonight and reduce stimulants after noon."
            )
        else:
            recommendations.append(
                "Behavioural adherence is very low. "
                "Focus on consistent meal timing and avoiding late-night activity."
            )

    elif readiness < 50:
        if weakest == "hrv":
            recommendations.append(
                "Moderate HRV suppression detected. "
                "Light activity only — walking or yoga. Avoid high-intensity training."
            )
        elif weakest == "sleep":
            recommendations.append(
                "Sleep regularity needs improvement. "
                "Aim for the same wake time tomorrow to anchor your biological clock."
            )
        else:
            recommendations.append(
                "Adherence to circadian routines is inconsistent. "
                "Prioritise meal timing and sleep schedule consistency."
            )

    elif readiness < 70:
        recommendations.append(
            "Moderate readiness — suitable for normal activity. "
            "Prioritise recovery tonight to improve tomorrow's score."
        )

    else:
        recommendations.append(
            "Good readiness — your autonomic recovery and sleep consistency "
            "are supporting performance. Maintain current routines."
        )

    return {
        "status": "success",
        "user_id": user_id,
        "readiness_score": readiness,
        "readiness_label": readiness_label(readiness),
        "drivers": {
            "avg_hrv":          avg_hrv,
            "alignment_score":  round(consistency_pct, 1),
            "adherence_score":  round(adherence_score, 1),
            "fatigue_prediction": fatigue_prediction,
            "risk_score":       data.get("risk_analysis", {}).get("risk_score", 0)
        },
        "driver_scores": {
            "hrv_score":            round(hrv_score, 1),
            "sleep_quality_score":  round(sleep_quality_score, 1),
            "adherence_score":      round(adherence_score, 1)
        },
        "weights": {
            "hrv":        "55% — autonomic recovery (Oura/Firstbeat methodology)",
            "sleep":      "28% — consistency + fatigue (Phillips et al. 2017)",
            "adherence":  "17% — behavioural patterns (Baron & Reid 2014)"
        },
        "recommendations": recommendations,
        "created_at": snapshot.get("created_at")
    }