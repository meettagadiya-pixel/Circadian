from datetime import datetime
from app.database.supabase_client import supabase

from app.analytics.digital_twin_engine import (
    calculate_user_digital_twin
)

from app.ml.features import (
    build_feature_vector
)



from app.analytics.personalization_engine import (
    analyze_intervention_effectiveness
)

from app.interventions.adaptive_engine import (
    rank_interventions
)

from app.analytics.anomaly_engine import (
    detect_physiological_anomalies
)

from app.analytics.risk_engine import (
    calculate_risk_state
)

from app.interventions.escalation_engine import (
    escalate_interventions
)

from app.interventions.recovery_protocols import (
    generate_recovery_protocol
)

from app.ingestion.junction_fetcher import (
    fetch_fitbit_activity,
    fetch_fitbit_sleep
)

from app.physiology.normalizer import (
    normalize_activity
)

from app.physiology.aggregator import (
    aggregate_physiology
)

from app.physiology.circadian import (
    estimate_circadian_phase
)

from app.physiology.misalignment import (
    calculate_misalignment
)

from app.analytics.circadian_trends import (
    analyze_circadian_trends
)

from app.interventions.circadian_interventions import (
    generate_circadian_interventions
)

from app.environment.light_cycle import (
    fetch_light_cycle
)

from app.behaviour.meal_timing import (
    analyze_meal_timing
)

from app.behaviour.exercise_timing import (
    analyze_exercise_timing
)

from app.interventions.contextual_engine import (
    generate_contextual_interventions
)

from app.interventions.orchestrator import (
    prioritize_interventions
)

from app.interventions.scheduler import (
    schedule_interventions
)

from app.ingestion.unified_ingestion import (
    get_provider_user_id
)
from app.analytics.adherence_engine import (
    calculate_adherence_score
)
from app.environment.light_exposure_analyzer import (
    analyze_light_exposure
)
from app.environment.daylight_analyzer import (
    analyze_daylight_context
)
from app.api.environment_context import (
    environment_context
)
from app.ingestion.junction_fetcher import (
    fetch_fitbit_hrv,
    fetch_fitbit_heartrate,
    fetch_fitbit_steps,
    fetch_freestyle_libre_glucose
)

from app.ingestion.junction_parser import (
    summarize_junction_timeseries
)

def run_physiology_pipeline():

    print(
        f"[{datetime.utcnow()}] "
        "Running physiology pipeline"
    )

    users_resp = (
        supabase
        .table("users")
        .select("*")
        .execute()
    )

    users = users_resp.data
    if not users:

        print(
            "No users found. Pipeline skipped."
        )

        return



    for user in users:
        try:
            user_id = user["id"]
            junction_user_id = (
                get_provider_user_id(
                    user_id=user_id,
                    provider="junction"
                )
            )

            if not junction_user_id:

                print(
                    f"No Junction user found for {user_id}. Skipping."
                )

                continue

            print(
                f"Processing user: {user_id}"
            )

            # ---------------------------------
            # REAL WEARABLE INGESTION
            # ---------------------------------

            activity_response = (
                fetch_fitbit_activity(
                    junction_user_id
                )
            )

            sleep_response = (
                fetch_fitbit_sleep(
                    junction_user_id
                )
            )

            activity_data = (
                activity_response["data"]
                .get("activity", [])
            )

            sleep_data = (
                sleep_response["data"]
                .get("sleep", [])
            )

            print(
                "Fetched activity:",
                len(activity_data)
            )

            print(
                "Fetched sleep:",
                len(sleep_data)
            )

            provider_user_id = (
                get_provider_user_id(
                    user_id
                )
            )

            junction_hrv = (
                summarize_junction_timeseries(
                    fetch_fitbit_hrv(
                        provider_user_id
                    )
                )
            )

            junction_heartrate = (
                summarize_junction_timeseries(
                    fetch_fitbit_heartrate(
                        provider_user_id
                    )
                )
            )

            junction_steps = (
                summarize_junction_timeseries(
                    fetch_fitbit_steps(
                        provider_user_id
                    )
                )
            )

            junction_glucose = (
                summarize_junction_timeseries(
                    fetch_freestyle_libre_glucose(
                        provider_user_id
                    )
                )
            )

            # ---------------------------------
            # NORMALIZATION
            # ---------------------------------

            normalized_activity = []

            for item in activity_data:

                normalized_activity.append(
                    normalize_activity(
                        item
                    )
                )

            physiology_summary = (
                aggregate_physiology(
                    normalized_activity
                )
            )

            # ---------------------------------
            # DATABASE DATA
            # Moved up so behavioral_logs are
            # available for true misalignment calc
            # ---------------------------------

            phys_resp = (
                supabase
                .table("physiological_data")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

            bio_resp = (
                supabase
                .table("biochemical_data")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

            behavior_resp = (
                supabase
                .table("behavioral_logs")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

            environmental_resp = (
                supabase
                .table(
                    "environmental_data"
                )
                .select("*")
                .eq(
                    "user_id",
                    user["id"]
                )
                .execute()
            )

            environmental_rows = (
                environmental_resp.data
            )

            # ---------------------------------
            # CIRCADIAN ANALYSIS
            # ---------------------------------

            circadian_analysis = []

            for item in sleep_data:

                circadian_analysis.append(
                    estimate_circadian_phase(
                        item
                    )
                )

            # Quick biological midnight estimate from
            # sleep midpoints — used so we can calculate
            # true misalignment before the digital twin runs
            quick_bio_midnight = None
            if circadian_analysis:
                midpoints = [
                    item.get("sleep_midpoint")
                    for item in circadian_analysis
                    if item.get("sleep_midpoint")
                ]
                if midpoints:
                    quick_bio_midnight = sorted(midpoints)[-1]

            # TRUE MISALIGNMENT:
            # Now calculates the real social vs biological
            # clock gap using sleep_onset from behavioral logs
            misalignment = (
                calculate_misalignment(
                    circadian_analysis,
                    behavioral_logs=behavior_resp.data,
                    biological_midnight=quick_bio_midnight
                )
            )

            trends = (
                analyze_circadian_trends(
                    circadian_analysis
                )
            )

            environmental = (
                fetch_light_cycle()
            )

            

            # ---------------------------------
            # ML FEATURES
            # ---------------------------------

            features = (
                build_feature_vector(
                    physiological_rows=phys_resp.data,
                    biochemical_rows=bio_resp.data,
                    behavioral_rows=behavior_resp.data
                )
            )

            features["avg_hrv"] = (
                junction_hrv.get("avg")
                or
                features.get("avg_hrv")
            )

            features["avg_rhr"] = (
                junction_heartrate.get("avg")
                or
                features.get("avg_rhr")
            )

            features["steps"] = (
                junction_steps.get("avg")
            )

            libre_avg_glucose = (
                junction_glucose.get("avg")
            )

            if libre_avg_glucose:

                features["avg_glucose"] = round(
                    libre_avg_glucose * 18,
                    2
                )

                features["max_glucose"] = round(
                    junction_glucose.get(
                        "max",
                        0
                    ) * 18,
                    2
                )

            # ---------------------------------
            # DIGITAL TWIN
            # ---------------------------------

            twin = (
                calculate_user_digital_twin(
                    user=user,
                    physiological_rows=phys_resp.data,
                    behavioral_rows=behavior_resp.data,
                    biochemical_rows=bio_resp.data,
                    glucose_override={
                        "avg_glucose":
                            features.get("avg_glucose"),

                        "max_glucose":
                            features.get("max_glucose"),

                        "glucose_variability":
                            features.get(
                                "glucose_std",
                                0
                            )
                    }
                )
            )

            print(
                f"Biological midnight: "
                f"{twin['circadian_phase']['biological_midnight']}"
            )

            meal_timing = (
                analyze_meal_timing(
                    behavior_resp.data,
                    twin["circadian_phase"][
                        "biological_midnight"
                    ]
                )
            )

            exercise_timing = (
                analyze_exercise_timing(
                    behavior_resp.data,
                    twin["circadian_phase"][
                        "biological_midnight"
                    ]
                )
            )

            adherence = (
                calculate_adherence_score(
                    behavioral_logs=behavior_resp.data,
                    biological_midnight=twin["circadian_phase"][
                        "biological_midnight"
                    ]
                )
            )

            biological_midnight = (
                twin["circadian_phase"][
                    "biological_midnight"
                ]
            )

            light_exposure_analysis = (
                analyze_light_exposure(
                    environmental_rows,
                    biological_midnight
                )
            )

            location_resp = (
                supabase
                .table("user_locations")
                .select("*")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )

            location = (
                location_resp.data[0]
                if location_resp.data
                else {
                    "latitude": 51.5072,
                    "longitude": -0.1276
                }
            )

            environmental_context = (
                environment_context(

                    latitude=location.get(
                        "latitude"
                    ),

                    longitude=location.get(
                        "longitude"
                    )
                )
            )

            daylight_context = (
                analyze_daylight_context(

                    sunrise=
                        environmental_context.get(
                            "sunrise"
                        ),

                    sunset=
                        environmental_context.get(
                            "sunset"
                        ),

                    biological_midnight=
                        biological_midnight,

                    clouds=
                        environmental_context.get(
                            "clouds"
                        ),

                    uvi=
                        environmental_context.get(
                            "uvi"
                        ),

                    weather=
                        environmental_context.get(
                            "weather"
                        )
                )
            )

            # ─────────────────────────────────────────────────
            # FATIGUE PREDICTION
            # Transparent HRV-based formula replacing ML model.
            # Based on published HRV-fatigue correlation research
            # (Karolinska Sleepiness Scale / Firstbeat methodology).
            #
            # Base score from HRV:
            #   >50ms = low fatigue (1)
            #   35-50ms = mild fatigue (2)
            #   20-35ms = moderate fatigue (3)
            #   10-20ms = high fatigue (4)
            #   <10ms = severe fatigue (5)
            #
            # Modifiers:
            #   + misalignment > 3h adds 1 point
            #   + consistency_score < 0.4 adds 1 point
            # Cap at 5.
            # ─────────────────────────────────────────────────

            avg_hrv_val = features.get("avg_hrv", 0) or 0

            if avg_hrv_val > 50:
                prediction = 1
            elif avg_hrv_val > 35:
                prediction = 2
            elif avg_hrv_val > 20:
                prediction = 3
            elif avg_hrv_val > 10:
                prediction = 4
            else:
                prediction = 5

            # Modifier: high misalignment worsens fatigue
            misalignment_hrs = misalignment.get(
                "misalignment_hours",
                misalignment.get("misalignment_score", 0)
            ) if misalignment else 0

            if misalignment_hrs > 3:
                prediction = min(5, prediction + 1)

            # Modifier: irregular sleep schedule worsens fatigue
            consistency = misalignment.get(
                "consistency_score", 1
            ) if misalignment else 1

            if consistency < 0.4:
                prediction = min(5, prediction + 1)

            print(
                f"Fatigue prediction: "
                f"{prediction}"
            )

            # Generate circadian interventions here where all context is available
            risk_obj = twin.get("risk_analysis") or twin.get("risk") or {}
            circadian_interventions = (
                generate_circadian_interventions(
                    misalignment=misalignment,
                    circadian_analysis=circadian_analysis,
                    environmental=environmental_context,
                    circadian_phase=twin["circadian_phase"],
                    metabolic_analysis=twin.get("metabolic_analysis"),
                    light_exposure_analysis=light_exposure_analysis,
                    adherence=adherence,
                    risk_state=risk_obj.get("risk_state", "moderate")
                )
            )

            contextual_interventions = (
                generate_contextual_interventions(

                    meal_timing=
                        meal_timing,

                    exercise_timing=
                        exercise_timing,

                    misalignment=
                        misalignment,

                    recovery_score=
                        features.get(
                            "avg_hrv",
                            0
                        ) / 100,

                    light_exposure_analysis=
                        light_exposure_analysis,

                    circadian_phase=
                        twin["circadian_phase"],

                    environmental=
                        environmental_context,

                    adherence=
                        adherence
                )
            )

            # ---------------------------------
            # INTERVENTIONS
            # ---------------------------------

            zeitgebers = twin.get(
                "zeitgebers",
                []
            )

            feedback_resp = (
                supabase
                .table("intervention_outcomes")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

            personalization_data = (
                analyze_intervention_effectiveness(
                    feedback_resp.data
                )
            )

            ranked_zeitgebers = (
                rank_interventions(
                    zeitgebers,
                    personalization_data
                )
            )

            combined_interventions = (
                ranked_zeitgebers
                +
                circadian_interventions
            )

            # ---------------------------------
            # ANOMALY ANALYSIS
            # ---------------------------------

            snapshot_resp = (
                supabase
                .table("digital_twin_snapshots")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=False)
                .limit(30)
                .execute()
            )

            anomaly_analysis = (
                detect_physiological_anomalies(
                    snapshot_resp.data
                )
            )

            # ---------------------------------
            # RISK ANALYSIS
            # Use true misalignment hours for
            # more accurate risk scoring
            # ---------------------------------

            metabolic = twin[
                "metabolic_analysis"
            ]

            risk = calculate_risk_state(
                anomaly_analysis=anomaly_analysis,
                fatigue_prediction=prediction,
                misalignment_hours=misalignment.get(
                    "misalignment_hours",
                    misalignment.get("midpoint_variability", 0)
                ),
                glucose_variability=metabolic[
                    "glucose_variability"
                ]
            )

            # ---------------------------------
            # ESCALATION
            # ---------------------------------

            final_zeitgebers = (
                escalate_interventions(
                    combined_interventions,
                    risk["risk_state"]
                )
            )

            final_zeitgebers.extend(
                contextual_interventions
            )

            final_zeitgebers = (
                prioritize_interventions(
                    final_zeitgebers
                )
            )

            light_cycle = (
                fetch_light_cycle()
            )

            scheduled_interventions = (
                schedule_interventions(

                    interventions=
                        final_zeitgebers,

                    circadian_phase=
                        twin[
                            "circadian_phase"
                        ],

                    sunrise_data=
                        light_cycle
                )
            )

            # ---------------------------------
            # RECOVERY PROTOCOL
            # ---------------------------------

            recovery_protocol = (
                generate_recovery_protocol(
                    risk["risk_state"]
                )
            )

            print(
                f"Generated "
                f"{len(final_zeitgebers)} "
                f"interventions."
            )

            # ---------------------------------
            # JSON CLEANER
            # ---------------------------------

            def clean_json(obj):

                if isinstance(obj, dict):

                    return {
                        k: clean_json(v)
                        for k, v in obj.items()
                    }

                elif isinstance(obj, list):

                    return [
                        clean_json(v)
                        for v in obj
                    ]

                elif hasattr(obj, "item"):

                    return obj.item()

                return obj

            # ---------------------------------
            # SNAPSHOT PAYLOAD
            # ---------------------------------

            snapshot_payload = clean_json({

                "user_id":
                    user_id,

                "biological_midnight":
                    twin["circadian_phase"][
                        "biological_midnight"
                    ],

                "fatigue_prediction":
                    int(prediction),

                "intervention_count":
                    int(len(final_zeitgebers)),

                "avg_hrv":
                    float(
                        features.get(
                            "avg_hrv",
                            0
                        )
                    ),

                "avg_glucose":
                    float(
                        features.get(
                            "avg_glucose",
                            0
                        )
                    ),

                "snapshot_data": {

                    "digital_twin":
                        twin,

                    "wearable_physiology":
                        physiology_summary,

                    "circadian_analysis":
                        circadian_analysis,

                    "misalignment":
                        misalignment,

                    "trend_analysis":
                        trends,

                    "features":
                        features,

                    "data_sources": {
                        "hrv": "junction_fitbit",
                        "heart_rate": "junction_fitbit",
                        "steps": "junction_fitbit",
                        "sleep": "junction_fitbit",
                        "activity": "junction_fitbit",
                        "glucose": "junction_freestyle_libre",
                        "weather": "openweathermap",
                        "light_exposure": "phone_sensor_or_manual",
                        "behavior": "manual_logs"
                    },

                    "zeitgebers":
                        final_zeitgebers,

                    "personalization":
                        personalization_data,

                    "risk_analysis":
                        risk,

                    "anomaly_analysis":
                        anomaly_analysis,

                    "recovery_protocol":
                        recovery_protocol,

                    "meal_timing":
                        meal_timing,

                    "daylight_context":
                        daylight_context,

                    "exercise_timing":
                        exercise_timing,

                    "adherence":
                        adherence,

                    "light_exposure_analysis":
                        light_exposure_analysis,

                    "contextual_interventions":
                        contextual_interventions,

                    "scheduled_interventions":
                        scheduled_interventions,
                }
            })

            supabase.table(
                "digital_twin_snapshots"
            ).insert(
                snapshot_payload
            ).execute()

            print(
                "Digital twin saved."
            )

        except Exception as error:

            print(
                f"Pipeline failed "
                f"for user "
                f"{user.get('id')}: "
                f"{error}"
            )

    # ─────────────────────────────────────────────────
    # SNAPSHOT CLEANUP — runs after all users processed
    # Keep only the 48 most recent snapshots per user
    # (48 minutes of history). Prevents unbounded DB growth.
    # ─────────────────────────────────────────────────
    try:
        users_for_cleanup = (
            supabase
            .table("users")
            .select("id")
            .execute()
        )

        for u in (users_for_cleanup.data or []):
            uid = u["id"]
            all_snaps = (
                supabase
                .table("digital_twin_snapshots")
                .select("id")
                .eq("user_id", uid)
                .order("created_at", desc=True)
                .execute()
            )
            snap_ids = [r["id"] for r in (all_snaps.data or [])]
            ids_to_delete = snap_ids[48:]
            if ids_to_delete:
                supabase.table("digital_twin_snapshots")                     .delete()                     .in_("id", ids_to_delete)                     .execute()

    except Exception as cleanup_err:
        print(f"Snapshot cleanup warning: {cleanup_err}")

    print(
        "Pipeline complete."
    )