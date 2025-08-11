from abc import ABC, abstractmethod
from typing import ClassVar

from src.domain.entities.github.repository import GithubRepository


class IGithubFetcher(ABC):
    _BASE_API_URL: ClassVar[str]
    _GITHUB_API_VERSION: ClassVar[str]

    @abstractmethod
    def clone_repository(self, link: str) -> GithubRepository:
        pass
