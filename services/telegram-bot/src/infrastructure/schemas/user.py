from src.infrastructure.schemas.base import CodeReviewSchema


class UserSchema(CodeReviewSchema):
    id: int
    name: str
    username: str | None
    language_code: str | None
    is_bot: bool | None = None
    is_premium: bool | None = None
