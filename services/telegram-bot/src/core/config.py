from functools import cached_property
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class CodeReviewerSetting(BaseSettings):
    ENABLE_LOGGER: bool
    ENABLE_COLORED_LOGS: bool

    BOT_TOKEN: str
    OUTER_BOT_PORT: int
    INNER_BOT_PORT: int

    @cached_property
    def kafka_bootstrap_server(self) -> str:
        return f"kafka:{self.KAFKA_DOCKER_PORT}"

    class Config:
        env_file = BASE_DIR / ".env"


config = CodeReviewerSetting()
