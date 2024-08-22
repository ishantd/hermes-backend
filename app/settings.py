import os
from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings
from yarl import URL

from app import constants

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """
    Application settings. Defaults to production. YOLO!
    """

    # fastapi + uvicorn
    workers_count: int = 1  # quantity of workers for uvicorn
    reload: bool = False  # Enable uvicorn reloading
    proxy_headers: bool = True  # Enable proxy headers for uvicorn
    host: str = "0.0.0.0"
    port: int = 8000
    secret_key: str = "this-is-a-secret"

    # database
    db_name: str = "hermes"
    db_user: str = "hermes"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = "5432"
    db_echo: bool = False

    # basics
    env: str = constants.PRODUCTION
    debug: bool = False

    @property
    def frontend_url(self):
        """
        Frontend URL for the application.
        """
        if self.env == constants.PRODUCTION:
            return "https://hermes.ishantdahiya.com"
        else:
            return "http://127.0.0.1:3000"

    @property
    def hermes_base_url(self):
        if self.env == constants.PRODUCTION:
            return "https://hermes-api.ishantdahiya.com"
        else:
            return "http://127.0.0.1:8000"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql",
            path=f"/{self.db_name}",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


def _parse_env() -> str:
    TESTING_VARS = ["TEST", "TESTING"]
    PRODUCTION_VARS = ["PRD", "PROD", "PRODUCTION"]

    os_env = os.environ.get("ENV")

    os_env = constants.PRODUCTION if os_env is None else os_env.upper()

    if os_env in PRODUCTION_VARS:
        os_env = constants.PRODUCTION
    elif os_env in TESTING_VARS:
        os_env = constants.TESTING
    else:
        os_env = constants.DEVELOPMENT

    return os_env


@lru_cache  # Make sure that we are reading from the env, disk only once
def _get_settings():
    os_env = _parse_env()
    settings = Settings(env=os_env)
    if settings.env == constants.TESTING:
        settings = Settings(
            env=os_env,
            db_name="hermes_test",
            db_user="hermes",
        )
    return settings


settings = _get_settings()
