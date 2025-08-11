from typing import Any


class GithubLicense:
    def __init__(self, data: dict[str, Any]) -> None:
        unknown = "Unknown"
        self.name = data.get("name", unknown)
        self.key = data.get("key", unknown)
