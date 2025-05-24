from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from django.forms.widgets import Select

from db.requests import decrease_shopping_cart, increase_shopping_cart
from dialogs.catalog_dialog.states import CatalogSG
from dialogs.shopping_cart.states import ShoppingCartSG


async def back(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if widget.widget_id == 'back_to_categories':
        dialog_manager.start_data['subcategory_page_id'] = 0

    if widget.widget_id == 'back_to_subcategory':
        dialog_manager.start_data.update({'items_page_id': 0, 'item_count': 0})

    await dialog_manager.back()


async def choose_category(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id,
):
    dialog_manager.dialog_data.update({'selected_category': item_id})
    await dialog_manager.switch_to(state=CatalogSG.subcategories)


async def choose_subcategory(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id,
):
    dialog_manager.dialog_data.update({'selected_subcategory': item_id})
    await dialog_manager.switch_to(state=CatalogSG.items)


async def update_shopping_cart(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    item_data = dialog_manager.dialog_data.get('selected_item_data')
    if widget.widget_id == 'confirm_cart_add':
        await increase_shopping_cart(
            tg_id=callback.from_user.id,
            item_id=item_data['id'],
            amount=dialog_manager.start_data.get('item_amount'),
        )
        await dialog_manager.back()

    elif widget.widget_id == 'cart_out':
        await decrease_shopping_cart(
            user_id=callback.from_user.id,
            item_id=item_data['id'],
        )


async def open_shopping_cart(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(
        state=ShoppingCartSG.main_page, data={'items_page_id': 0}
    )
