from aiogram import Bot
from aiogram.types import Message

from src.core.logger import Logger
from src.domain.entities.user import UserEntity
from src.domain.interfaces.services.auth import IAuthService

logger = Logger.setup(__name__)


class AuthService(IAuthService):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def authenticate(self, ref_code: str | None, msg: Message) -> None:
        data = self._get_user_data(msg=msg)
        await self._handle_user(data=data)

        if ref_code:
            await self._notify_referrer(ref_code=ref_code, data=data, msg=msg)

    async def _handle_user(self, data: UserEntity) -> None:
        # request to api for authenticating user in the system
        logger.info(f"[AuthService]: User {data.id} was authenticated.")

    async def _notify_referrer(
            self,
            ref_code: str,
            data: UserEntity,
            msg: Message
    ) -> None:
        if not ref_code.isdigit():
            return

        formatted_username = (
            f"<a href='tg://user?id={msg.from_user.id}'>{data.name}</a>"
            if not data.username
            else f"@{data.username}"
        )
        await self.bot.send_message(
            chat_id=ref_code,
            text=f"👥 <b>{formatted_username}</b> used your referral code!"
        )

    @classmethod
    def _get_user_data(cls, msg: Message) -> UserEntity:
        return UserEntity(
            id=msg.from_user.id,
            name=msg.from_user.first_name,
            username=msg.from_user.username,
            language_code=msg.from_user.language_code,
            is_bot=msg.from_user.is_bot,
            is_premium=msg.from_user.is_premium,
        )
