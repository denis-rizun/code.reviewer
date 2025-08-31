from types import TracebackType
from typing import TypeVar

MessageType = TypeVar("MessageType")
FSMContextType = TypeVar("FSMContextType")
ExcType = type[BaseException] | None
ExcVal = BaseException | None
ExcTB = TracebackType | None
