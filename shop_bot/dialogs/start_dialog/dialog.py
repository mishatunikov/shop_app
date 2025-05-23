from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next, Row
from aiogram_dialog.widgets.text import Format

from dialogs.start_dialog.getters import main_menu_getter, reference_getter
from dialogs.start_dialog.handlers import start_next_dialog
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
        Next(Format('{reference_button}')),
        getter=main_menu_getter,
        state=StartSG.main_menu,
    ),
    Window(
        Format('{reference_text}'),
        Back(Format('{main_menu_button}')),
        getter=reference_getter,
        state=StartSG.reference,
    ),
)
