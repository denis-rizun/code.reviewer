from json import dumps

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiokafka import AIOKafkaProducer
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from src.application.auth import AuthService
from src.core.config import config
from src.infrastructure.bot.configurator import BotConfigurator
from src.infrastructure.kafka.consumer import KafkaConsumerFactory, KafkaConsumer
from src.infrastructure.kafka.manager import KafkaManager
from src.infrastructure.kafka.publisher import KafkaPublisher


class Container(DeclarativeContainer):
    bot = Singleton(
        Bot,
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    storage = Singleton(MemoryStorage)
    dispatcher = Singleton(Dispatcher, storage=storage)
    bot_configurator = Singleton(
        BotConfigurator,
        bot=bot,
        dispatcher=dispatcher,
    )

    auth_service = Factory(AuthService, bot=bot)

    kafka_producer = Singleton(
        AIOKafkaProducer,
        bootstrap_servers=config.kafka_bootstrap_server,
        value_serializer=lambda v: dumps(v).encode(),
        key_serializer=lambda k: k.encode() if k else None,
    )
    kafka_consumer_factory = Singleton(
        KafkaConsumerFactory,
        bootstrap_servers=config.kafka_bootstrap_server,
    )
    kafka_publisher = Singleton(
        KafkaPublisher,
        producer=kafka_producer
    )
    kafka_consumer = Factory(KafkaConsumer)
    kafka_manager = Factory(
        KafkaManager,
        publisher=kafka_publisher,
        consumer=kafka_consumer
    )


container = Container()
