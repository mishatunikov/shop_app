from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

CURRENT_PATH = Path(__file__).resolve().parent


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            'ru': ('ru',),
        },
        [
            FluentTranslator(
                locale='ru',
                translator=FluentBundle.from_files(
                    locale='ru-RU',
                    filenames=[
                        str(CURRENT_PATH / 'ru/LC_MESSAGES/lexicon.ftl'),
                        str(CURRENT_PATH / 'ru/LC_MESSAGES/buttons.ftl'),
                    ],
                ),
            )
        ],
        root_locale='ru',
    )
    return translator_hub
