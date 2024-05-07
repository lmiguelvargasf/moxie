from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    USE_TEST_DB: bool = False

    @property
    def db_url(self) -> str:
        url = self.DATABASE_URL.unicode_string()
        return url


settings = Settings()
