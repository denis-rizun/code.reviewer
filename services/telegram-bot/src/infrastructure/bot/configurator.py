from aiogram import Dispatcher, Bot
from dependency_injector.wiring import inject, Provide

from src.presentation.handlers import router
from src.infrastructure.bot.middlewares import CleanupMessageMiddleware


class BotConfigurator:
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self.bot = bot
        self.dispatcher = dispatcher

    @inject
    async def run(self, auth_service = Provide["auth_service"]) -> None:
        self.dispatcher.workflow_data.update(bot=self.bot, auth_service=auth_service)
        self.dispatcher.include_router(router=router)
        self.dispatcher.message.middleware(CleanupMessageMiddleware())

        await self.dispatcher.start_polling(self.bot)
