from app.ingestion.synthetic_data import (
    generate_mock_physiology
)

from app.ingestion.vital_adapter import (
    fetch_vital_data
)

from app.ingestion.apple_health_adapter import (
    fetch_apple_health_data
)

from app.ingestion.oura_adapter import (
    fetch_oura_data
)

from app.database.supabase_client import (
    supabase
)

def get_provider_user_id(
    user_id,
    provider="junction"
):

    response = (
        supabase
        .table(
            "user_provider_connections"
        )
        .select(
            "provider_user_id"
        )
        .eq(
            "user_id",
            user_id
        )
        .eq(
            "provider",
            provider
        )
        .limit(1)
        .execute()
    )

    if not response.data:

        raise Exception(
            f"No provider mapping found "
            f"for {provider}"
        )

    return response.data[0][
        "provider_user_id"
    ]


def get_user_physiology(
    user_id,
    provider="synthetic"
):

    # -------------------------
    # VITAL
    # -------------------------

    if provider == "vital":

        vital = fetch_vital_data(
            user_id
        )

        if vital["connected"]:

            return {
                "source": "vital",
                "data": vital["data"]
            }

    # -------------------------
    # APPLE HEALTH
    # -------------------------

    elif provider == "apple_health":

        apple = fetch_apple_health_data(
            user_id
        )

        if apple["connected"]:

            return {
                "source":
                    "apple_health",

                "data":
                    apple["data"]
            }

    # -------------------------
    # OURA
    # -------------------------

    elif provider == "oura":

        oura = fetch_oura_data(
            user_id
        )

        if oura["connected"]:

            return {
                "source": "oura",
                "data": oura["data"]
            }

    # -------------------------
    # SYNTHETIC FALLBACK
    # -------------------------

    mock_data = (
        generate_mock_physiology(
            user_id
        )
    )

    return {
        "source": "synthetic",
        "data": mock_data
    }