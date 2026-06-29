from datetime import datetime, timezone
from dateutil.parser import parse


def calculate_misalignment(circadian_analysis, behavioral_logs=None, biological_midnight=None):
    """
    Calculates two distinct misalignment metrics:

    1. TRUE MISALIGNMENT (social vs biological clock gap):
       The average difference in hours between when the user
       actually falls asleep (sleep_onset from behavioral logs)
       and their biological midnight (from circadian phase).
       This is what Andreas described — the real social vs bio clock gap.

    2. CONSISTENCY SCORE:
       How variable the sleep midpoint is across days.
       Kept as a separate metric — tells a different story.
    """

    # ─────────────────────────────────────────────────
    # PART 1: TRUE MISALIGNMENT
    # Using sleep_onset from behavioral_logs vs biological_midnight
    # ─────────────────────────────────────────────────

    true_misalignment_hours = None

    if behavioral_logs and biological_midnight:

        try:
            bio_midnight_dt = parse(str(biological_midnight))

            if bio_midnight_dt.tzinfo is None:
                bio_midnight_dt = bio_midnight_dt.replace(tzinfo=timezone.utc)

            # Get the hour of biological midnight (e.g. 03:16 = 3.27)
            bio_hour = bio_midnight_dt.hour + bio_midnight_dt.minute / 60

            # Collect all sleep_onset events
            sleep_onsets = [
                log for log in behavioral_logs
                if log.get("event_type") == "sleep_onset"
            ]

            if sleep_onsets:

                gap_hours = []

                for log in sleep_onsets:

                    ts = parse(str(log["timestamp"]))

                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)

                    sleep_hour = ts.hour + ts.minute / 60

                    # Calculate the circular gap between sleep onset
                    # and biological midnight on the 24h clock
                    # e.g. sleep at 21:30, bio midnight at 03:16
                    # gap = 03.27 - 21.50 = -18.23 → wrap → 5.77h
                    raw_gap = bio_hour - sleep_hour

                    # Wrap to [-12, 12] range for circular time
                    if raw_gap > 12:
                        raw_gap -= 24
                    elif raw_gap < -12:
                        raw_gap += 24

                    # We want absolute gap in hours
                    gap_hours.append(abs(raw_gap))

                if gap_hours:
                    true_misalignment_hours = round(
                        sum(gap_hours) / len(gap_hours), 2
                    )

        except Exception as e:
            print(f"[misalignment] True misalignment calculation error: {e}")
            true_misalignment_hours = None

    # ─────────────────────────────────────────────────
    # PART 2: CONSISTENCY SCORE
    # How variable is sleep midpoint across days?
    # ─────────────────────────────────────────────────

    if not circadian_analysis:
        return {
            "avg_midpoint_hour": 0,
            "midpoint_variability": 0,
            "consistency_score": 0,
            "misalignment_score": true_misalignment_hours or 0,
            "misalignment_hours": true_misalignment_hours or 0,
            "misalignment_type": "true_social_bio_gap" if true_misalignment_hours else "variability_proxy",
            "interpretation": _interpret_misalignment(true_misalignment_hours or 0)
        }

    midpoint_hours = []

    for item in circadian_analysis:

        midpoint = item.get("sleep_midpoint")

        if not midpoint:
            continue

        try:
            midpoint_dt = datetime.fromisoformat(str(midpoint))
            hour = midpoint_dt.hour + midpoint_dt.minute / 60
            midpoint_hours.append(hour)
        except Exception:
            continue

    if not midpoint_hours:
        avg_midpoint = 0
        variability = 0
    else:
        avg_midpoint = sum(midpoint_hours) / len(midpoint_hours)
        variability = max(midpoint_hours) - min(midpoint_hours)

    consistency_score = max(0, round(1 - (variability / 6), 2))

    # Use true misalignment if available, fall back to variability proxy
    final_misalignment = true_misalignment_hours if true_misalignment_hours is not None else round(min(variability / 4, 1.0), 2)

    return {
        "avg_midpoint_hour": round(avg_midpoint, 2),
        "midpoint_variability": round(variability, 2),
        "consistency_score": consistency_score,

        # This is the REAL misalignment — social vs biological clock
        "misalignment_score": final_misalignment,
        "misalignment_hours": final_misalignment,

        # So the dashboard can show the right label
        "misalignment_type": "true_social_bio_gap" if true_misalignment_hours is not None else "variability_proxy",

        # Human-readable interpretation for the frontend
        "interpretation": _interpret_misalignment(final_misalignment)
    }


def _interpret_misalignment(hours):
    """
    Converts a misalignment score in hours into a
    human-readable clinical interpretation.
    """
    if hours is None:
        return "No data"
    if hours < 1:
        return "Well aligned — social and biological clocks are in sync"
    if hours < 2:
        return "Mild misalignment — minor circadian disruption"
    if hours < 3:
        return "Moderate misalignment — circadian stress likely"
    if hours < 5:
        return "High misalignment — significant social jetlag detected"
    return "Severe misalignment — chronic circadian disruption risk"
