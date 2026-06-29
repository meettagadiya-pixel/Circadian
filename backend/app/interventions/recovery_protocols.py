def generate_recovery_protocol(
    risk_state
):

    if risk_state == "low":

        return {
            "recovery_focus":
                "maintenance",

            "protocol": [
                "Maintain current sleep schedule.",
                "Continue stable meal timing.",
                "Keep regular light exposure."
            ]
        }

    elif risk_state == "moderate":

        return {
            "recovery_focus":
                "stabilization",

            "protocol": [
                "Prioritize earlier sleep timing.",
                "Increase morning outdoor light.",
                "Reduce late-night eating.",
                "Lower evening screen exposure."
            ]
        }

    elif risk_state == "high":

        return {
            "recovery_focus":
                "aggressive_recovery",

            "protocol": [
                "Reduce cognitive overload.",
                "Increase sleep opportunity tonight.",
                "Avoid intense late exercise.",
                "Hydrate consistently.",
                "Strictly avoid circadian disruption."
            ]
        }

    else:

        return {
            "recovery_focus":
                "critical_recovery",

            "protocol": [
                "Maximize recovery behaviors immediately.",
                "Strongly reduce physiological stress.",
                "Prioritize extended sleep.",
                "Avoid alcohol and metabolic stress.",
                "Maintain low stimulation environment."
            ]
        }