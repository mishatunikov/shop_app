import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub

from config import Config, load_config
from dialogs import catalog_dialog, shopping_cart_dialog, start_dialog
from handlers.user_handlers import router as user_router
from locales.i18n import create_translator_hub
from middlewares.outer import TranslatorRunnerMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Запуск бота')

    config: Config = load_config()
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    translator_hub: TranslatorHub = create_translator_hub()

    dp = Dispatcher()
    dp.workflow_data.update({'_translator_hub': translator_hub})

    logger.info('Покдлючение роутеров и диалогов')
    dp.include_routers(
        user_router, start_dialog, catalog_dialog, shopping_cart_dialog
    )
    setup_dialogs(dp)

    logger.info('Подключение миддлварей')
    dp.update.middleware(TranslatorRunnerMiddleware())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
