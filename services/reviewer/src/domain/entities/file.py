from dataclasses import dataclass


@dataclass
class FileRepositoryMetaContent:
    description: str
    readme: str
    actions: str
    content: dict[str, str]
    imports: dict[str, str]
