import asyncio
from collections.abc import Awaitable
from typing import Callable, ClassVar

from aiokafka import AIOKafkaConsumer

from src.core.logger import Logger
from src.domain.interfaces.broker.consumer import IConsumer, IConsumerFactory
from src.infrastructure.kafka.base import KafkaBroker

logger = Logger.setup(__name__)


class KafkaConsumer(KafkaBroker, IConsumer):
    _TYPE: ClassVar[str] = "consumer"

    def __init__(self) -> None:
        self._consumers: dict[str, AIOKafkaConsumer] = {}
        self._tasks: list[asyncio.Task] = []
        self._logger = logger
        super().__init__()

    async def start(self) -> None:
        self._started = True
        await super().start()

    async def stop(self) -> None:
        for consumer in self._consumers.values():
            await consumer.stop()

        for task in self._tasks:
            task.cancel()

        self._started = False
        await super().stop()

    async def consume(
            self,
            topic: str,
            handler: Callable[[str | None, dict], Awaitable[None]],
            factory: IConsumerFactory | None,
    ) -> None:
        if not self._started:
            raise RuntimeError("KafkaConsumer must be started before consuming")

        consumer = factory.create(topic=topic)
        await consumer.start()
        self._consumers[topic] = consumer

        async def _consume_loop():
            async for msg in consumer:
                try:
                    await handler(msg.key, msg.value)
                except Exception as e:
                    self._logger.exception(f"Error while handling Kafka message: {e}")

        task = asyncio.create_task(_consume_loop(), name=f"kafka-consume-{topic}")
        self._tasks.append(task)
