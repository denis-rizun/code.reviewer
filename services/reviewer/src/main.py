import asyncio

from src.application.message_handler import MessageHandler
from src.core.constants import Constants
from src.infrastructure.di.bootstrap import Bootstrap
from src.infrastructure.di.container import container


async def main() -> None:
    await Bootstrap.wire()

    handler = MessageHandler(container=container)
    consumer = container.kafka_consumer()
    async with consumer:
        for topic in Constants.TOPIC_MAPPER.keys():
            await consumer.add_consumer(
                topic=topic,
                group=Constants.TOPIC_MAPPER[topic]["group"],
                handler=handler.handle,
            )

        await consumer.start_consuming()


if __name__ == "__main__":
    asyncio.run(main())
