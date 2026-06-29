import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    VITAL_API_KEY: str = os.getenv("VITAL_API_KEY", "")
    VITAL_BASE_URL: str = os.getenv("VITAL_BASE_URL", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")


settings = Settings()