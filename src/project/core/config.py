from pydantic_settings import BaseSettings
from pydantic import SecretStr
from pydantic import ValidationError

#from dotenv import load_dotenv
#load_dotenv()

class Settings(BaseSettings):
    ORIGINS: str = "*"
    ROOT_PATH: str = ""
    ENV: str = "DEV"
    LOG_LEVEL: str = "DEBUG"

    POSTGRES_SCHEMA: str = "public"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5678
    POSTGRES_USER: SecretStr = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    # JWT tokens
    JWT_SECRET_KEY: SecretStr = "b2b2j2bj234bn2bj23bn23sajk3279sfd4bn324b3243bj324324bb32n324bhq0"
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


try:
    settings = Settings()
    print("Настройки успешно загружены.")
except ValidationError as e:
    print("Ошибка валидации:", e)
