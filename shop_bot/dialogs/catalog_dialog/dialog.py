from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Next,
    Row,
    Select,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format

from dialogs.catalog_dialog.getters import (
    categories_getter,
    item_cart_add_getter,
    items_getter,
    subcategories_getter,
)
from dialogs.catalog_dialog.handlers import (
    back,
    change_item_amount,
    change_page,
    choose_category,
    choose_subcategory,
    show_alert_increase,
    update_shopping_cart,
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
                on_click=choose_category,
            )
        ),
        Row(
            Button(
                Format('{previous}'),
                id='category_previous_page',
                when='previous_page_exist',
                on_click=change_page,
            ),
            Button(
                Format('{next}'),
                id='category_next_page',
                when='next_page_exist',
                on_click=change_page,
            ),
        ),
        Cancel(Format('{main_menu}'), id='main_menu'),
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
                on_click=choose_subcategory,
            )
        ),
        Row(
            Button(
                Format('{previous}'),
                id='subcategory_previous_page',
                when='previous_page_exist',
                on_click=change_page,
            ),
            Button(
                Format('{next}'),
                id='subcategory_next_page',
                when='next_page_exist',
                on_click=change_page,
            ),
        ),
        Button(Format('{back}'), id='back_to_categories', on_click=back),
        state=CatalogSG.subcategories,
        getter=subcategories_getter,
    ),
    Window(
        Format('{counter}'),
        Format('{item_info}'),
        StaticMedia(path=Format('{image}'), type=ContentType.PHOTO),
        Row(
            Button(
                Format('{previous}'),
                id='previous_item',
                when='previous_item_exist',
                on_click=change_page,
            ),
            Button(
                Format('{next}'),
                id='next_item',
                when='next_item_exist',
                on_click=change_page,
            ),
        ),
        Row(
            Button(
                Format('{minus}'),
                id='decrease_amount',
                on_click=change_item_amount,
                when='has_previous_item',
            ),
            Button(
                Format('{minus}'),
                id='decrease_count_alert',
                on_click=show_alert_increase,
                when='cannot_decrease',
            ),
            Button(
                Format('{item_amount}'), id='item_amount', when='not_in_cart'
            ),
            Button(
                Format('{plus}'),
                id='increase_amount',
                on_click=change_item_amount,
                when='not_in_cart',
            ),
        ),
        Next(
            Format('{cart_add}'),
            id='cart_add',
            when='not_in_cart',
        ),
        Button(Format('{is_added}'), id='is_added', when='item_in_cart'),
        # Button(
        #     Format('{cart_out}'),
        #     id='cart_out',
        #     when='item_in_cart',
        #     on_click=update_shopping_cart,
        # ),
        Button(Format('{shopping_cart}'), id='shopping_cart'),
        Button(Format('{back}'), id='back_to_subcategories', on_click=back),
        state=CatalogSG.items,
        getter=items_getter,
    ),
    Window(
        Format('{cart_add_answer}\n'),
        Format('{item_info}'),
        StaticMedia(path=Format('{image}'), type=ContentType.PHOTO),
        Row(
            Back(Format('{cancel}')),
            Button(
                Format('{confirm}'),
                id='confirm_cart_add',
                on_click=update_shopping_cart,
            ),
        ),
        state=CatalogSG.confirm_item_cart_add,
        getter=item_cart_add_getter,
    ),
)
