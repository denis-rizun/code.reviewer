from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.domain.enums.path import PathEnum


class KeyboardGetter:

    @staticmethod
    def main_without_back() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=PathEnum.REVIEW),
                    KeyboardButton(text=PathEnum.DONATION),
                    KeyboardButton(text=PathEnum.SUPPORT),
                ]
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def back() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=PathEnum.BACK)
                ]
            ],
            resize_keyboard=True,
        )
