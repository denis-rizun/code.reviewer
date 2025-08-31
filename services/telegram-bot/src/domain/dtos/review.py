from dataclasses import dataclass
from typing import Self

from src.domain.enums.review import ReviewStatusEnum


@dataclass
class ReviewRequestDTO:
    task_id: str
    repository_link: str


@dataclass
class ReviewResponseDataDTO:
    task_id: str
    overview: str
    repository_link: str


@dataclass
class ReviewResponseDTO:
    status: ReviewStatusEnum
    data: ReviewResponseDataDTO | None = None

    @classmethod
    def validate(cls, obj: dict[str, str]) -> Self:
        data = (
            ReviewResponseDataDTO(
                task_id=obj["task_id"],
                overview=obj["overview"],
                repository_link=obj["repository_link"],
            )
            if obj["status"] == ReviewStatusEnum.READY.value
            else None
        )
        return ReviewResponseDTO(
            status=obj["status"],
            data=data,
        )
