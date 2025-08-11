from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar


class IGithubProcesser(ABC):
    EXCLUDED_DIRS: ClassVar[set]
    EXCLUDED_EXTENSIONS: ClassVar[set]

    @abstractmethod
    async def get_files_content(self, root_path: Path) -> dict[str, str]:
        pass

    @abstractmethod
    def get_files_count(self, content: dict[str, str]) -> int:
        pass

    @abstractmethod
    def get_readme(self, content: dict[str, str]) -> str | None:
        pass

    @abstractmethod
    def get_actions(self, content: dict[str, str]) -> str | None:
        pass
