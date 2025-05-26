from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Next, Row, Select
from aiogram_dialog.widgets.text import Format

from dialogs.general_handlers import back, change_page
from dialogs.start_dialog.getters import faq_getter, main_menu_getter
from dialogs.start_dialog.handlers import get_info, start_next_dialog
from dialogs.start_dialog.states import StartSG

start_dialog = Dialog(
    Window(
        Format('{main_menu_text}'),
        Row(
            Button(
                Format('{catalog_button}'),
                id='catalog',
                on_click=start_next_dialog,
            ),
            Button(
                Format('{shopping_cart_button}'),
                id='shopping_cart',
                on_click=start_next_dialog,
            ),
        ),
        Next(Format('{faq_button}')),
        getter=main_menu_getter,
        state=StartSG.main_menu,
    ),
    Window(
        Format('{faq_text}'),
        Column(
            Select(
                Format('{item[0]}'),
                id='questions',
                item_id_getter=lambda x: x[1],
                items='questions',
                on_click=get_info,
            )
        ),
        Row(
            Button(
                Format('{previous}'),
                id='faq_previous_page',
                when='previous_page_exist',
                on_click=change_page,
            ),
            Button(
                Format('{next}'),
                id='faq_next_page',
                when='next_page_exist',
                on_click=change_page,
            ),
        ),
        Button(
            Format('{main_menu_button}'), on_click=back, id='back_from_faq'
        ),
        getter=faq_getter,
        state=StartSG.faq,
    ),
)
