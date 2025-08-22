from json import dumps, loads, JSONDecodeError
from typing import Any

from src.core.exceptions import SerializationException, DeserializationException
from src.core.logger import Logger
from src.domain.interfaces.serializer import ISerializer

logger = Logger.setup(__name__)


class JSONSerializer(ISerializer):

    @classmethod
    def serialize(cls, obj: Any) -> bytes:
        try:
            return dumps(obj, ensure_ascii=False).encode('utf-8')
        except (TypeError, ValueError) as e:
            logger.error(f"Serialization error: {e}")
            raise SerializationException(f"Serialization error: {e}")

    @classmethod
    def deserialize(cls, obj: bytes) -> Any:
        if obj is None:
            return None

        try:
            return loads(obj.decode('utf-8'))
        except (UnicodeDecodeError, JSONDecodeError) as e:
            logger.error(f"Deserialization error: {e}")
            raise DeserializationException(f"Deserialization error: {e}")
