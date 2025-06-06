from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner


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

    if widget.widget_id in (
        widget_offset := {
            'faq_previous_page': -1,
            'faq_next_page': 1,
        }
    ):
        dialog_manager.start_data['faq_page_id'] += widget_offset[
            widget.widget_id
        ]


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


async def back(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if widget.widget_id == 'back_to_categories':
        dialog_manager.start_data['subcategory_page_id'] = 0

    if widget.widget_id == 'back_to_subcategory':
        dialog_manager.start_data.update({'items_page_id': 0, 'item_count': 0})

    if widget.widget_id in (
        'number_input_back',
        'city_input_back',
        'street_input_back',
        'house_input_back',
        'flat_input_back',
    ):
        if data := dialog_manager.dialog_data.get('delivery_data_messages'):
            data.pop()

    if widget.widget_id == 'back_from_faq':
        dialog_manager.start_data.update({'faq_page_id': 0})

    await dialog_manager.back()
