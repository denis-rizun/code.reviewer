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
    rating: str
    repository_link: str


@dataclass
class ReviewResponseDTO:
    status: ReviewStatusEnum
    data: ReviewResponseDataDTO | None = None

    @classmethod
    def validate(cls, obj: dict[str, str]) -> Self:
        return ReviewResponseDTO(
            status=obj["status"],
            data=ReviewResponseDataDTO(
                task_id=obj["data"],
                rating=obj["rating"],
                repository_link=obj["repository_link"],
            ),
        )
