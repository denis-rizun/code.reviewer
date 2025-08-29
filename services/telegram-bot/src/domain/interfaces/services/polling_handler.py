from abc import ABC, abstractmethod
from typing import Callable

from src.domain.enums.progress import ProgressTypeEnum
from src.domain.type import MessageType


class IPollingHandler(ABC):
    
    @abstractmethod
    async def show_progress(
        self, 
        message: MessageType,
        check_status_callback: Callable,
        initial_text: str,
        progress_type: ProgressTypeEnum,
    ) -> list[int]:
        pass
