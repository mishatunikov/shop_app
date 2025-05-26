from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, List

from dialogs.general_handlers import (
    change_item_amount,
    change_page,
    show_alert_increase,
)
from dialogs.shopping_cart.getters import (
    cart_main_page_getter,
    change_cart_getter,
    change_item_amount_getter,
    confirmation_getter,
)
from dialogs.shopping_cart.handlers import (
    change_shopping_cart,
    clean_cart,
    confirm_amount_changing,
    remove_item,
    place_order,
    show_confirm_alert,
)
from dialogs.shopping_cart.states import ShoppingCartSG

shopping_cart_dialog = Dialog(
    Window(
        Format('{shopping_cart_empty}', when='cart_is_empty'),
        Format('{shopping_cart_text}\n', when='items'),
        List(
            field=Format('<b>{item[0]}</b>. {item[1]}'),
            items='items',
            when='items',
        ),
        Format('{items_total_price}', when='items'),
        Button(
            Format('{make_order_button}'),
            id='make_order',
            when='items',
            on_click=place_order,
        ),
        Button(
            Format('{change_cart_button}'),
            on_click=change_shopping_cart,
            id='update_cart',
            when='items',
        ),
        SwitchTo(
            Format('{clean_cart_button}'),
            state=ShoppingCartSG.clean_cart_confirmation,
            when='items',
            id='clean_cart',
        ),
        Cancel(Format('{main_menu_button}'), id='main_menu'),
        state=ShoppingCartSG.main_page,
        getter=cart_main_page_getter,
    ),
    Window(
        Format('{confirmation_text}'),
        Button(
            Format('{confirm_button}'),
            id='confirm_clean_cart',
            on_click=clean_cart,
        ),
        SwitchTo(
            Format('{cancel_button}'),
            state=ShoppingCartSG.main_page,
            id='cancel_clean_cart',
        ),
        state=ShoppingCartSG.clean_cart_confirmation,
        getter=confirmation_getter,
    ),
    Window(
        Format('{counter}\n'),
        Format('{item_info}\n'),
        Format('{amount_info}'),
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
        SwitchTo(
            Format('{change_amount_button}'),
            state=ShoppingCartSG.change_item_count,
            id='change_amount_item',
        ),
        SwitchTo(
            Format('{cart_item_out}'),
            state=ShoppingCartSG.delete_item_confirmation,
            id='cart_item_out',
        ),
        SwitchTo(
            Format('{back}'),
            state=ShoppingCartSG.main_page,
            id='cancel_change_cart',
        ),
        state=ShoppingCartSG.change_cart,
        getter=change_cart_getter,
    ),
    Window(
        Format('{confirmation_text}\n'),
        StaticMedia(path=Format('{image}'), type=ContentType.PHOTO),
        Format('{item_info}'),
        Button(
            Format('{confirm_button}'),
            id='confirm_delete_item',
            on_click=remove_item,
        ),
        SwitchTo(
            Format('{cancel_button}'),
            state=ShoppingCartSG.change_cart,
            id='cancel_delete_item',
        ),
        state=ShoppingCartSG.delete_item_confirmation,
        getter=confirmation_getter,
    ),
    Window(
        Format('{change_amount_text}'),
        Row(
            Button(
                Format('{minus}'),
                id='decrease_amount',
                on_click=change_item_amount,
                when='not_minimal',
            ),
            Button(
                Format('{minus}'),
                id='decrease_count_alert',
                on_click=show_alert_increase,
                when='cannot_decrease',
            ),
            Button(
                Format('{item_amount}'),
                id='item_amount',
            ),
            Button(
                Format('{plus}'),
                id='increase_amount',
                on_click=change_item_amount,
            ),
        ),
        Button(
            Format('{confirm_button}'),
            id='confirm_change',
            when='new_amount',
            on_click=confirm_amount_changing,
        ),
        Button(
            Format('{confirm_button}'),
            id='cannot_confirm',
            when='not_new_amount',
            on_click=show_confirm_alert,
        ),
        SwitchTo(
            Format('{cancel_button}'),
            state=ShoppingCartSG.change_cart,
            id='cancel_change_amount',
        ),
        state=ShoppingCartSG.change_item_count,
        getter=change_item_amount_getter,
    ),
)
