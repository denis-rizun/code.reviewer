from aiokafka.errors import KafkaError

from src.core.exceptions import NotInitializedException
from src.core.logger import Logger
from src.domain.interfaces.broker.factory import IFactory
from src.domain.interfaces.broker.producer import IProducer

logger = Logger.setup(__name__)


class KafkaProducer(IProducer):
    def __init__(self, factory: IFactory) -> None:
        self._factory = factory
        self._producer = None
        self._started = False

    async def send(self, topic: str, key: str | None, value: dict) -> None:
        if not self._started or self._producer is None:
            raise NotInitializedException("Producer is not initialized or started")

        try:
            await self._producer.send_and_wait(topic=topic, key=key, value=value)
        except KafkaError as e:
            logger.error(f"Kafka send error: {e}")

    async def _start(self) -> None:
        if not self._started:
            self._producer = self._factory.create()
            await self._producer.start()
            self._started = True

    async def _stop(self) -> None:
        self._started = False
        if self._producer:
            await self._producer.stop()
