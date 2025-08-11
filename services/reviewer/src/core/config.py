from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ENABLE_LOGGER: bool
    ENABLE_COLORED_LOGS: bool

    GITHUB_TOKEN: str
    DEEPSEEK_API_KEY: str

    @staticmethod
    def repo_path(name: str) -> Path:
        return BASE_DIR / "repos" / name

    class Config:
        env_file = BASE_DIR / ".env"


config = Settings()
