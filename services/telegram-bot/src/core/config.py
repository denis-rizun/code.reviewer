from functools import cached_property
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class CodeReviewerSetting(BaseSettings):
    PROJECT_NAME: str = "code.reviewer"
    GITHUB_LINK: str = "https://github.com/denis-rizun/code.reviewer"
    ENABLE_LOGGER: bool
    ENABLE_COLORED_LOGS: bool

    BOT_TOKEN: str
    OUTER_BOT_PORT: int
    INNER_BOT_PORT: int

    ZOOKEEPER_VERSION: str
    KAFKA_VERSION: str
    ZOOKEEPER_CLIENT_PORT: int
    ZOOKEEPER_TICK_TIME: int
    KAFKA_BROKER_ID: int
    OUTER_KAFKA_PORT: int
    INNER_KAFKA_PORT: int
    KAFKA_DOCKER_PORT: int
    KAFKA_REPLICATION_FACTOR: int

    @cached_property
    def kafka_bootstrap_server(self) -> str:
        # return f"localhost:{self.KAFKA_DOCKER_PORT}"
        return "localhost:9092"

    class Config:
        env_file = BASE_DIR / ".env"


config = CodeReviewerSetting()
