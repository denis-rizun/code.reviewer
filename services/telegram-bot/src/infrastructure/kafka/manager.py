from typing import Self

from src.core.logger import Logger
from src.domain.interfaces.broker.consumer import IConsumer
from src.domain.interfaces.broker.publisher import IPublisher

logger = Logger.setup(__name__)


class KafkaManager:
    def __init__(self, publisher: IPublisher, consumer: IConsumer) -> None:
        self.publisher = publisher
        self.consumer = consumer

    async def __aenter__(self) -> Self:
        await self.publisher.start()
        await self.consumer.start()
        return self

    async def __aexit__(
            self,
            exc_type: BaseException | None,
            exc_val: BaseException | None,
            exc_tb: object | None
    ) -> None:
        await self.publisher.stop()
        await self.consumer.stop()

    @classmethod
    async def message_handler(cls, key: str | None) -> None:
        logger.info(f"[KafkaManager]: Received message with {key=}")
