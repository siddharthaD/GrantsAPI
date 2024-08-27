from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")
    PGSQL_URL: str = "sqlite:///data/grants.db"
    APP_SEED_DATA: bool = False
    JWT_SECRET_KEY: str = "UNDERSECRETARY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRY: int = 30


app_settings = AppSettings()
