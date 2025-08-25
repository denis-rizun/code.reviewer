import os
from typing import Any, ClassVar
from uuid import uuid4

from git import Repo
from httpx import get

from src.core.config import config
from src.core.logger import Logger
from src.domain.entities.github.repository import GithubRepository
from src.domain.interfaces.repository.cloner import IRepositoryCloner

logger = Logger.setup(__name__)


class GitHubCloner(IRepositoryCloner):
    _BASE_API_URL: ClassVar[str] = "https://api.github.com/repos"
    _API_VERSION: ClassVar[str] = "2022-11-28"

    def clone(self, link: str) -> GithubRepository:
        data = self._request(owner=link.split("/")[-2], repo=link.split("/")[-1])
        repo = GithubRepository.transform(data=data)

        while True:
            name = str(uuid4())
            local_path = config.repo_path(name)
            if not os.path.exists(local_path):
                break

        Repo.clone_from(url=repo.clone_url, to_path=local_path)
        repo.local_path = local_path
        logger.info(f"[GitHubCloner]: Repository {repo.full_name} cloned to {name}.")
        return repo

    def _request(self, owner: str, repo: str) -> dict[str, Any]:
        url = f"{self._BASE_API_URL}/{owner}/{repo}"
        response = get(url=url, headers=self._get_headers)
        response.raise_for_status()
        return response.json()

    @property
    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "X-GitHub-Api-Version": self._API_VERSION
        }
