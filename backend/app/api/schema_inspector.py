from fastapi import APIRouter

from app.database.supabase_client import supabase

router = APIRouter()


@router.get("/inspect-schema")
def inspect_schema():

    tables = [
        "users",
        "physiological_data",
        "biochemical_data",
        "environmental_data",
        "behavioral_logs"
    ]

    results = {}

    for table in tables:

        try:

            response = (
                supabase
                .table(table)
                .select("*")
                .limit(1)
                .execute()
            )

            if response.data:

                results[table] = {
                    "exists": True,
                    "sample_row": response.data[0]
                }

            else:

                results[table] = {
                    "exists": True,
                    "sample_row": None
                }

        except Exception as e:

            results[table] = {
                "exists": False,
                "error": str(e)
            }

    return results