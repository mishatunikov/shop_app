from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.catalog_dialog.states import CatalogSG


async def start_next_dialog(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    id_state = {'catalog': CatalogSG.categories, 'shopping_cart': ...}

    await dialog_manager.start(
        state=id_state.get(widget.widget_id), data={'page_number': 1}
    )
