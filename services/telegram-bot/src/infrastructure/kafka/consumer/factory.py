from json import loads

from aiokafka import AIOKafkaConsumer

from src.domain.enums.consume import ConsumeTypeEnum
from src.domain.interfaces.broker.consumer import IConsumerFactory


class KafkaConsumerFactory(IConsumerFactory[AIOKafkaConsumer]):
    def __init__(
            self,
            bootstrap_servers: str,
            auto_offset_reset: ConsumeTypeEnum = ConsumeTypeEnum.EARLIEST,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._auto_offset_reset = auto_offset_reset.value

    def create(self, topic: str, group_id: str) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=group_id,
            key_deserializer=lambda k: k.decode("utf-8") if k else None,
            value_deserializer=lambda v: loads(v.decode("utf-8")),
            auto_offset_reset=self._auto_offset_reset,
        )
