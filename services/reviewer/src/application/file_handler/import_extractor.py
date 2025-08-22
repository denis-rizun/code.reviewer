import re
from pathlib import Path
from typing import ClassVar

from src.domain.interfaces.import_extractor import IImportExtractor


class ImportExtractor(IImportExtractor):
    _IMPORT_PATTERNS: ClassVar[dict[str, str]] = {
        "python": r"^(?:from\s+\S+\s+import\s+\S+|import\s+\S+)",
        "go": r"^(?:import\s+\(.*?\)|import\s+\"[^\"]+\")",
        "javascript": r"^(?:import\s+.*?from\s+['\"].+?['\"]|require\s*\(.*?\))",
        "typescript": r"^(?:import\s+.*?from\s+['\"].+?['\"]|require\s*\(.*?\))",
        "java": r"^import\s+[\w\.]+;",
        "php": r"^(?:use\s+[\w\\]+;|require(?:_once)?\s*\(.*?\);|include(?:_once)?\s*\(.*?\);)",
        "ruby": r"^(?:require\s+['\"].+?['\"]|require_relative\s+['\"].+?['\"])",
        "c_cpp": r"^#\s*include\s+[<\"].+[>\"]",
        "csharp": r"^using\s+[\w\.]+;",
        "rust": r"^(?:use\s+[\w:]+(?:\s+as\s+\w+)?;|extern\s+crate\s+\w+;)",
    }
    _EXT_MAP: ClassVar[dict[str, str]] = {
        ".py": "python",
        ".go": "go",
        ".js": "javascript",
        ".mjs": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".php": "php",
        ".rb": "ruby",
        ".c": "c_cpp",
        ".h": "c_cpp",
        ".cpp": "c_cpp",
        ".hpp": "c_cpp",
        ".cs": "csharp",
        ".rs": "rust",
    }

    def extract(self, files: dict[str, str]) -> dict[str, str]:
        imports_by_file = {}

        for filepath, code in files.items():
            ext = Path(filepath).suffix.lower()
            lang = self._EXT_MAP.get(ext)
            if not lang:
                continue

            pattern = self._IMPORT_PATTERNS.get(lang)
            if not pattern:
                continue

            extracted_lines = []
            for line in code.splitlines():
                stripped = line.strip()
                if re.match(pattern, stripped):
                    extracted_lines.append(stripped)

            if extracted_lines:
                imports_by_file[filepath] = "\n".join(extracted_lines)

        return imports_by_file
