from dataclasses import dataclass
from typing import Any, Self

from src.core.constants import Constants
from src.domain.entities.github.license import GithubLicense
from src.domain.entities.github.owner import GithubOwner


@dataclass
class GithubRepository:
    name: str
    full_name: str
    is_private: bool
    owner: GithubOwner
    url: str
    description: str
    clone_url: str
    local_path: str
    stars: int
    watchers: int
    language: str
    licence: GithubLicense
    default_branch: str

    @classmethod
    def transform(cls, data: dict[str, Any]) -> Self:
        return cls(
            name=data.get("name", Constants.UNKNOWN_ELLIPSE),
            full_name=data.get("full_name", Constants.UNKNOWN_ELLIPSE),
            is_private=data.get("private", False),
            owner=GithubOwner.transform(data=data.get("owner", {})),
            url=data.get("html_url", Constants.UNKNOWN_ELLIPSE),
            description=data.get("description", Constants.UNKNOWN_ELLIPSE),
            clone_url=data.get("clone_url", Constants.UNKNOWN_ELLIPSE),
            local_path=Constants.UNKNOWN_ELLIPSE,
            stars=data.get("stargazers_count", 0),
            watchers=data.get("watchers", 0),
            language=data.get("language", Constants.UNKNOWN_ELLIPSE),
            licence=GithubLicense.transform(data=data.get("license", {})),
            default_branch=data.get("default_branch", Constants.UNKNOWN_ELLIPSE),
        )
