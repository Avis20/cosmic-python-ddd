from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_PASS: str = 'cosmic-pass'
    DB_USER: str = 'cosmic-user'
    DB_NAME: str = 'cosmic'

    API_HOST: str = 'localhost'
    API_PORT: int = 5005

    @property
    def get_postgres_uri(self):
        return (
            f"postgres://{self.DB_NAME}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def get_api_url(self):
        return f"http://{self.API_HOST}:{self.API_PORT}"


def get_settings():
    return Settings()
