from os import walk, path
from pathlib import Path

from aiofiles import open

from src.domain.interfaces.repository.processer import IFileProcesser


class FileProcesser(IFileProcesser):
    EXCLUDED_DIRS = {"__pycache__", ".git", ".venv"}
    EXCLUDED_EXTENSIONS = {".pyc", ".lock", ".docx", ".json", ".csv", ".session"}

    async def get_files_content(self, root_path: Path) -> dict[str, str]:
        result = {}

        for dirpath, dirnames, filenames in walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in self.EXCLUDED_DIRS]
            dirpath = Path(dirpath)  # noqa
            for filename in filenames:
                file_path = dirpath / filename
                relative_path = path.relpath(file_path, start=root_path)

                if file_path.suffix.lower() in self.EXCLUDED_EXTENSIONS:
                    continue

                try:
                    async with open(file_path, encoding='utf-8') as f:
                        content = await f.read()
                        result[relative_path] = content

                except (UnicodeDecodeError, OSError):
                    continue

        return result

    def get_files_count(self, content: dict[str, str]) -> int:
        return len(content.keys())

    def get_readme(self, content: dict[str, str]) -> str | None:
        found = content.get("README.md")
        if found:
            return found
        else:
            return content.get("readme.md")

    def get_actions(self, content: dict[str, str]) -> str | None:
        actions = []
        for file_path, cnt in content.items():
            if file_path.startswith(".github") or file_path.startswith(".gitlab"):
                actions.append(f"\n--- {path} ---\n{cnt}\n")

        return "".join(actions) if actions else None
