from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from django.forms.widgets import Select

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


async def back(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if widget.widget_id == 'back_to_categories':
        dialog_manager.start_data['subcategory_page_id'] = 0
    await dialog_manager.back()


async def change_menu_level(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id,
):
    dialog_manager.dialog_data.update({'selected_category': item_id})
    await dialog_manager.switch_to(state=CatalogSG.subcategories)
