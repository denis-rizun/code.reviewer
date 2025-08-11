from typing import Any

from src.domain.entities.github.license import GithubLicense
from src.domain.entities.github.owner import GithubOwner


class GithubRepository:
    def __init__(self, data: dict[str, Any]) -> None:
        unknow = "Unknown"
        self.name = data.get("name", unknow)
        self.full_name = data.get("full_name", unknow)
        self.is_private = data.get("private", False)
        self.owner = GithubOwner(data=data.get("owner", {}))
        self.url = data.get("html_url", unknow)
        self.description = data.get("description", unknow)
        self.clone_url = data.get("clone_url", unknow)
        self.local_path = unknow
        self.stars = data.get("stargazers_count", 0)
        self.watchers = data.get("watchers", 0)
        self.language = data.get("language", unknow)
        self.licence = GithubLicense(data=data.get("license", {}))
        self.default_branch = data.get("default_branch", unknow)
