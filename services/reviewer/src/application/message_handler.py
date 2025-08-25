from src.core.constants import Constants
from src.core.exceptions import NotFoundException
from src.core.logger import Logger

logger = Logger.setup(__name__)


class MessageHandler:
    def __init__(self, container: "Container") -> None:  # noqa
        self._container = container

    async def handle(self, topic: str, key: str, value: dict) -> None:
        logger.debug(f"Received message: topic={topic} key={key} value={value}")
        mapped_topic = Constants.TOPIC_MAPPER[topic]
        if not mapped_topic:
            logger.error(f"Topic {topic} not found in TOPIC_MAPPER")
            raise NotFoundException(f"Topic {topic} not found in TOPIC_MAPPER")

        service_name = mapped_topic["service"]
        service_method = mapped_topic["method"]

        service = self._get_service_by_name(name=service_name)
        if not hasattr(service, service_method):
            logger.error(f"Method {service_method} not found in {service_name}")
            raise NotFoundException(
                f"Method {service_method} not found in {service_name}"
            )

        found_method = getattr(service, service_method)
        await found_method(key, value)

    def _get_service_by_name(self, name: str) -> object:
        try:
            provider = getattr(self._container, name)
            return provider()
        except AttributeError as e:
            logger.error(f"Service '{name}' not found in container")
            raise NotFoundException(f"Service '{name}' not found in container") from e
