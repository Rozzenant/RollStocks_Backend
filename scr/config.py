from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        url = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"\
                    f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url

    class Config:
        env_file = ".env"


settings = Settings()
