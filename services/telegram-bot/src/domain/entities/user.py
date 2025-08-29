from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
    name: str
    username: str | None
    language_code: str | None
    is_bot: bool | None = None
    is_premium: bool | None = None
