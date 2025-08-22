from dataclasses import dataclass
from typing import Any, Self

from src.core.constants import Constants


@dataclass
class GithubOwner:
    id: int
    username: str
    avatar: str

    @classmethod
    def transform(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data.get("id", 0),
            username=data.get("login", Constants.UNKNOWN_ELLIPSE),
            avatar=data.get("avatar_url", Constants.UNKNOWN_ELLIPSE)
        )
