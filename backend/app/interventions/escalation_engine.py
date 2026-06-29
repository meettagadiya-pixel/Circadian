def escalate_interventions(
    zeitgebers,
    risk_state
):

    escalated = []

    urgency_map = {
        "moderate": "elevated",
        "high": "high",
        "critical": "critical"
    }

    # Specific escalation suffixes per intervention type
    # Instead of one generic message appended to everything
    type_suffix = {
        "light_exposure": {
            "high": " Start this morning.",
            "critical": " Do this as soon as possible today."
        },
        "sleep_timing": {
            "high": " Begin adjusting tonight.",
            "critical": " This is your highest priority change tonight."
        },
        "sleep_schedule": {
            "high": " Consistency starts tonight.",
            "critical": " Critical: set a fixed wake alarm for tomorrow."
        },
        "nutrition": {
            "high": " Avoid late carbohydrates tonight.",
            "critical": " Strict meal timing is essential right now."
        },
        "exercise_timing": {
            "high": " Shift your workout earlier starting today.",
            "critical": " No intense exercise within 4 hours of sleep."
        },
        "recovery": {
            "high": " Prioritise rest today.",
            "critical": " Reduce all physical and cognitive load today."
        },
        "morning_light": {
            "high": " Get outside within 30 minutes of waking.",
            "critical": " Morning light is your most important reset tool right now."
        },
        "evening_light_reduction": {
            "high": " Dim screens and lights from 9 PM.",
            "critical": " No bright screens after 9 PM — critical for recovery."
        },
        "phase_delay": {
            "high": " Prioritise morning light exposure.",
            "critical": " Your biological clock is significantly delayed."
        }
    }

    for item in zeitgebers:

        updated = item.copy()

        intervention_type = item.get(
            "type", ""
        )

        if risk_state == "moderate":

            updated["urgency"] = "elevated"
            updated["priority"] = updated.get(
                "priority", "medium"
            )

        elif risk_state == "high":

            updated["urgency"] = "high"
            updated["priority"] = "high"

            # Get type-specific suffix or generic
            suffix = (
                type_suffix
                .get(intervention_type, {})
                .get("high", " Prioritise this today.")
            )

            # Only append if not already ending with it
            if not updated["message"].endswith(suffix.strip()):
                updated["message"] += suffix

        elif risk_state == "critical":

            updated["urgency"] = "critical"
            updated["priority"] = "high"

            suffix = (
                type_suffix
                .get(intervention_type, {})
                .get("critical", " Immediate action required.")
            )

            if not updated["message"].endswith(suffix.strip()):
                updated["message"] += suffix

        else:

            updated["urgency"] = "normal"

        escalated.append(updated)

    return escalated
