from typing import ClassVar

from aiokafka import AIOKafkaProducer

from src.domain.interfaces.broker.publisher import IPublisher
from src.infrastructure.kafka.base import KafkaBroker


class KafkaPublisher(KafkaBroker, IPublisher):
    _TYPE: ClassVar[str] = "publisher"

    def __init__(self, producer: AIOKafkaProducer) -> None:
        self._producer = producer
        super().__init__()

    async def start(self) -> None:
        if not self._started:
            await self._producer.start()
            await super().start()

    async def stop(self) -> None:
        if self._started:
            await self._producer.stop()
            await super().start()

    async def publish(self, topic: str, key: str | None, value: dict) -> None:
        if not self._started:
            raise RuntimeError("KafkaPublisher must be started before publishing")

        await self._producer.send_and_wait(topic, key=key, value=value)
