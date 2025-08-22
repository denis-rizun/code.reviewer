from typing import Any
from src.core.exceptions import SerializationException, DeserializationException
from src.core.logger import Logger
from src.domain.interfaces.serializer import ISerializer

logger = Logger.setup(__name__)


class StringSerializer(ISerializer):

    @classmethod
    def serialize(cls, obj: Any) -> bytes:
        try:
            return str(obj).encode('utf-8')
        except (UnicodeEncodeError, AttributeError) as e:
            logger.error(f"Serialization error: {e}")
            raise SerializationException(f"Serialization error: {e}")

    @classmethod
    def deserialize(cls, obj: bytes | None) -> Any:
        if obj is None:
            return None

        if obj == b'':
            return None

        try:
            return obj.decode('utf-8')
        except (UnicodeDecodeError, AttributeError) as e:
            logger.error(f"Deserialization error: {e}")
            raise DeserializationException(f"Deserialization error: {e}")
