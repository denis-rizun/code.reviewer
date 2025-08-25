from enum import StrEnum


class ConsumeTypeEnum(StrEnum):
    EARLIEST = "earliest"
    LATEST = "latest"
    NONE = "none"
