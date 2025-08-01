from src.core.logger import Logger
from src.infrastructure.di.container import container

logger = Logger.setup(__name__)


class Bootstrap:

    @classmethod
    async def wire(cls) -> None:
        logger.info("[DI]: Wiring dependencies...")
        container.init_resources()
        container.wire(
            packages=[
                "src.infrastructure.bot.configurator",
                "src.application.auth",
            ]
        )
        logger.info("[DI]: Dependencies wired.")
