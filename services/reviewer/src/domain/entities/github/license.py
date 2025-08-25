from dataclasses import dataclass
from typing import Any, Self

from src.core.constants import Constants


@dataclass
class GithubLicense:
    name: str
    key: str

    @classmethod
    def transform(cls, data: dict[str, Any]) -> Self:
        return cls(
            name=data.get("name", Constants.UNKNOWN_ELLIPSE),
            key=data.get("key", Constants.UNKNOWN_ELLIPSE)
        )
