from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from fluentogram import TranslatorHub

import consts
from config import Config


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        hub: TranslatorHub = data.get('_translator_hub')
        data['i18n'] = hub.get_translator_by_locale(
            locale=consts.DEFAULT_LOCALE
        )
        return await handler(event, data)


class CheckSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[[Message], Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        config: Config = data.get('config')
        chat_member = await event.bot.get_chat_member(
            chat_id=config.bot.chanel, user_id=event.from_user.id
        )
        if chat_member.status == 'left':
            await event.answer(
                text=f'Подпишитесь на канал {config.bot.chanel}',
            )

        else:
            return await handler(event, data)
