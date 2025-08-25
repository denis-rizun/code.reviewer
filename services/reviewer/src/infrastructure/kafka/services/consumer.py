from asyncio import create_task, gather
from typing import Callable

from aiokafka.errors import KafkaError

from src.core.exceptions import NotInitializedException
from src.core.logger import Logger
from src.domain.interfaces.broker.consumer import IConsumer
from src.domain.interfaces.broker.factory import IFactory

logger = Logger.setup(__name__)


class KafkaConsumer(IConsumer):
    def __init__(self, factory: IFactory) -> None:
        self._factory = factory
        self._consumer_tasks = []
        self._consumers = {}
        self._tasks = []
        self._running = False

    async def add_consumer(self, topic: str, group: str, handler: Callable) -> None:
        task = create_task(
            self.consume(
                topic=topic,
                group=group,
                handler=handler,
                factory=self._factory
            )
        )
        self._consumer_tasks.append(task)

    async def consume(
            self,
            topic: str,
            group: str,
            handler: Callable,
            factory: IFactory,
    ) -> None:
        if not self._running:
            raise NotInitializedException(
                "KafkaConsumer must be started before consuming"
            )

        consumer = factory.create(topic=topic, group_id=group)
        await consumer.start()
        self._consumers[topic] = consumer

        async def consume_loop() -> None:
            try:
                async for msg in consumer:
                    try:
                        await handler(msg.topic, msg.key, msg.value)
                    except Exception as e:
                        logger.error(f"Handler error: {e}")
            except KafkaError as e:
                logger.error(f"Kafka consumer error: {e}")

        task = create_task(consume_loop(), name=f"consume-{topic}")
        self._tasks.append(task)
        await task

    async def start_consuming(self) -> None:
        if self._consumer_tasks:
            await gather(*self._consumer_tasks)

    async def _start(self) -> None:
        self._running = True

    async def _stop(self) -> None:
        self._running = False
        for consumer in self._consumers.values():
            await consumer.stop()

        for task in self._tasks:
            task.cancel()

        self._consumers.clear()
        self._tasks.clear()
