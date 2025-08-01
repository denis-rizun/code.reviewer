import asyncio

from src.core.logger import Logger
from src.domain.enums.topic import KafkaTopicEnum
from src.infrastructure.di.bootstrap import Bootstrap
from src.infrastructure.di.container import container

logger = Logger.setup(__name__)


async def main():
    await Bootstrap.wire()
    configurator = container.bot_configurator()
    kafka_manager = container.kafka_manager()
    async with kafka_manager:
        await configurator.run()
        await kafka_manager.consumer.consume(
            topic=KafkaTopicEnum.USER_ACTION,
            handler=kafka_manager.message_handler,
        )


if __name__ == "__main__":
    logger.info("[BOT]: Telegram Bot was started!")
    try:
        asyncio.run(main())
    finally:
        logger.info("[BOT]: Telegram Bot was stopped!")
