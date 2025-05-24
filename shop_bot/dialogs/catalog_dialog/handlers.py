from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from django.forms.widgets import Select
from fluentogram import TranslatorRunner

from db.requests import decrease_shopping_cart, increase_shopping_cart
from dialogs.catalog_dialog.states import CatalogSG


async def change_page(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    **kwargs,
):
    if widget.widget_id in (
        widget_offset := {
            'category_previous_page': -1,
            'category_next_page': 1,
        }
    ):
        dialog_manager.start_data['category_page_id'] += widget_offset[
            widget.widget_id
        ]
    if widget.widget_id in (
        widget_offset := {
            'subcategory_previous_page': -1,
            'subcategory_next_page': 1,
        }
    ):
        dialog_manager.start_data['subcategory_page_id'] += widget_offset[
            widget.widget_id
        ]

    if widget.widget_id in (
        widget_offset := {'previous_item': -1, 'next_item': 1}
    ):
        dialog_manager.start_data['items_page_id'] += widget_offset[
            widget.widget_id
        ]


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


async def change_item_amount(
    callback: CallbackQuery,
    widget: Button,
    dilog_manager: DialogManager,
):
    id_offset = {'increase_amount': 1, 'decrease_amount': -1}
    dilog_manager.start_data['item_amount'] += id_offset[widget.widget_id]


async def show_alert_increase(
    callback: CallbackQuery,
    widget: Button,
    dilog_manager: DialogManager,
):
    i18n: TranslatorRunner = dilog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.decrease.button.alert())


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
