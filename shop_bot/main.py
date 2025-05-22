import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config, load_config
from fluentogram import TranslatorHub
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
    dp.include_router(user_router)

    logger.info('Подключение миддлварей')
    dp.update.middleware(TranslatorRunnerMiddleware())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
