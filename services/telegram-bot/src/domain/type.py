from types import TracebackType
from typing import TypeVar

MessageType = TypeVar("MessageType")
ExcType = type[BaseException] | None
ExcVal = BaseException | None
ExcTB = TracebackType | None
