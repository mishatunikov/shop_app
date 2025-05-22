from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner


async def main_menu_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    i18n: TranslatorRunner,
    **kwargs,
):
    text_selection = int(bool(dialog_manager.start_data))

    if dialog_manager.start_data:
        dialog_manager.start_data.clear()

    return {
        'main_menu_text': i18n.main.menu.text(
            text_selection=text_selection, name=event_from_user.first_name
        ),
        'catalog_button': i18n.catalog.button(),
        'shopping_cart_button': i18n.shopping.cart.button(),
        'reference_button': i18n.reference.button(),
    }


async def reference_getter(i18n: TranslatorRunner, **kwargs):
    return {
        'reference_text': i18n.reference.text(),
        'main_menu_button': i18n.main.menu.button(),
    }
