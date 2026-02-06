from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    ADMIN_DB_URL: str
    TEST_DB_URL: str
    PROD_DB_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

setting = Settings()