from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres_password'
    DB_NAME: str = 'ticketsstorm'

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    class Config:
        env_file = '.env'
settings = Settings()