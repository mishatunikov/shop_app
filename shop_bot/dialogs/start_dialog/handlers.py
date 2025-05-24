from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

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
