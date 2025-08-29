from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from src.application.auth import AuthService
from src.application.review import ReviewService
from src.core.config import config
from src.infrastructure.bot.configurator import BotConfigurator
from src.infrastructure.bot.polling_handler import PollingMessageHandler


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
    polling_msg_handler = Factory(PollingMessageHandler)
    review_service = Factory(ReviewService, message_handler=polling_msg_handler)


container = Container()
