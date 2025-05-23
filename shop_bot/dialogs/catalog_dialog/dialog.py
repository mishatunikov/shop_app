from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Column,
    Row,
    Select,
)
from aiogram_dialog.widgets.text import Format

from dialogs.catalog_dialog.getters import (
    categories_getter,
    subcategories_getter,
)
from dialogs.catalog_dialog.handlers import (
    back,
    change_menu_level,
    change_page,
)
from dialogs.catalog_dialog.states import CatalogSG

catalog_dialog = Dialog(
    Window(
        Format('{categories_text}'),
        Column(
            Select(
                Format('{item[0]}'),
                id='categories',
                item_id_getter=lambda x: x[1],
                items='categories',
                on_click=change_menu_level,
            )
        ),
        Row(
            Button(
                Format('{previous}'),
                id='category_previous_page',
                when='previous_page_exist',
                on_click=change_page,
            ),
            Cancel(Format('{main_menu}'), id='main_menu'),
            Button(
                Format('{next}'),
                id='category_next_page',
                when='next_page_exist',
                on_click=change_page,
            ),
        ),
        state=CatalogSG.categories,
        getter=categories_getter,
    ),
    Window(
        Format('{subcategories_text}'),
        Column(
            Select(
                Format('{item[0]}'),
                id='subcategories',
                item_id_getter=lambda x: x[1],
                items='subcategories',
            )
        ),
        Row(
            Button(
                Format('{previous}'),
                id='subcategory_previous_page',
                when='previous_page_exist',
                on_click=change_page,
            ),
            Button(Format('{back}'), id='back_to_categories', on_click=back),
            Button(
                Format('{next}'),
                id='subcategory_next_page',
                when='next_page_exist',
                on_click=change_page,
            ),
        ),
        state=CatalogSG.subcategories,
        getter=subcategories_getter,
    ),
)
