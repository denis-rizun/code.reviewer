from typing import ClassVar

from src.core.logger import Logger
from src.domain.interfaces.broker.broker import IBroker

logger = Logger.setup(__name__)


class KafkaBroker(IBroker):
    _TYPE: ClassVar[str] = "broker"

    def __init__(self) -> None:
        self._started = False

    async def start(self) -> None:
        self._started = True
        logger.info(f"[KafkaBroker]: Kafka {self._TYPE} started.")

    async def stop(self) -> None:
        self._started = False
        logger.info(f"[KafkaBroker]: Kafka {self._TYPE} stopped.")
