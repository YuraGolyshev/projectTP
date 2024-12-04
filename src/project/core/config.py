from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    # TODO убрать значения по умолчанию при переносе приложения в Docker
    ORIGINS: str = "*"
    ROOT_PATH: str = ""
    ENV: str = "DEV"
    LOG_LEVEL: str = "DEBUG"

    POSTGRES_SCHEMA: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
