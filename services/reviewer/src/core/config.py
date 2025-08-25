from functools import cached_property
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ENABLE_LOGGER: bool
    ENABLE_COLORED_LOGS: bool

    PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    ZOOKEEPER_CLIENT_PORT: int
    KAFKA_BROKERS: str
    KAFKA_HOST_PORT: int
    KAFKA_UI_PORT: int
    KAFKA_DOCKER_PORT: int

    GITHUB_TOKEN: str
    DEEPSEEK_API_KEY: str

    @cached_property
    def kafka_bootstrap_server(self) -> str:
        return f"kafka:{self.KAFKA_DOCKER_PORT}"

    @staticmethod
    def repo_path(name: str) -> Path:
        return BASE_DIR / "temp" / name

    class Config:
        env_file = BASE_DIR / ".env"


config = Settings()
