from abc import ABC, abstractmethod

from src.domain.entities.github.repository import GithubRepository


class IRepositoryCloner(ABC):

    @abstractmethod
    def clone(self, link: str) -> GithubRepository:
        pass
