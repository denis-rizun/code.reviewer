from aiokafka import AIOKafkaConsumer

from src.domain.enums.consume import ConsumeTypeEnum
from src.domain.interfaces.broker.factory import IFactory
from src.domain.interfaces.serializer import ISerializer


class KafkaConsumerFactory(IFactory):
    def __init__(
            self,
            bootstrap_servers: str,
            key_serializer: ISerializer,
            value_serializer: ISerializer,
            auto_offset_reset: ConsumeTypeEnum = ConsumeTypeEnum.EARLIEST
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._key_serializer = key_serializer
        self._value_serializer = value_serializer
        self._auto_offset_reset = auto_offset_reset

    def create(self, topic: str | list[str], group_id: str) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=self._auto_offset_reset,
            key_deserializer=self._key_serializer.deserialize,
            value_deserializer=self._value_serializer.deserialize,
            enable_auto_commit=True,
        )
