from typing import Any


class GithubOwner:
    def __init__(self, data: dict[str, Any]) -> None:
        unknown = "Unknown"
        self.id = data.get("id", 0)
        self.username = data.get("login", unknown)
        self.avatar = data.get("avatar_url", unknown)
