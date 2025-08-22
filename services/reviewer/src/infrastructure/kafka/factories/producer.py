from aiokafka import AIOKafkaProducer

from src.domain.interfaces.broker.factory import IFactory
from src.domain.interfaces.serializer import ISerializer


class KafkaProducerFactory(IFactory):
    def __init__(
            self,
            bootstrap_servers: str,
            key_serializer: ISerializer,
            value_serializer: ISerializer,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._key_serializer = key_serializer
        self._value_serializer = value_serializer

    def create(self) -> AIOKafkaProducer:
        return AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            key_serializer=self._key_serializer.serialize,
            value_serializer=self._value_serializer.serialize,
        )
