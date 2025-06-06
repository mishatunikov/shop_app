from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from fluentogram import TranslatorRunner

from db.requests import get_answer
from dialogs.catalog_dialog.states import CatalogSG
from dialogs.shopping_cart.states import ShoppingCartSG


async def start_next_dialog(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    id_data = {
        'shopping_cart': (ShoppingCartSG.main_page, {}),
        'catalog': (
            CatalogSG.categories,
            {
                'category_page_id': 0,
                'subcategory_page_id': 0,
                'items_page_id': 0,
                'item_amount': 1,
            },
        ),
    }
    state, start_data = id_data.get(widget.widget_id)

    await dialog_manager.start(state=state, data=start_data)


async def get_info(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    answer = await get_answer(question=item_id)
    await callback.message.answer(
        text=i18n.question.answer(question=item_id, answer=answer)
    )
    await callback.message.delete()