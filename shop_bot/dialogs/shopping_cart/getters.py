from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from db.requests import get_shopping_cart_items
from dialogs.shopping_cart.states import ShoppingCartSG


async def cart_main_page_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
):
    items, is_exist, total_amount, total_price = await get_shopping_cart_items(
        tg_id=event_from_user.id
    )

    items_output = []
    items_amount = []

    for num, item in enumerate(items, start=1):
        items_amount.append((item.name, item.amount))
        items_output.append(
            (
                num,
                i18n.item.main.cart.page.text(
                    name=item.name,
                    amount=item.amount,
                    price=float(item.price),
                    total=item.total_item_price,
                )
                + '\n',
            )
        )

    dialog_manager.dialog_data.update(
        {'total_price': float(total_price), 'items_amount': items_amount}
    )
    return {
        'items': items_output,
        'shopping_cart_empty': i18n.shopping.cart.empty.text(),
        'shopping_cart_text': i18n.shopping.cart.text(
            items_amount=total_amount
        ),
        'cart_is_empty': not total_amount,
        'make_order_button': i18n.make.order.button(),
        'change_cart_button': i18n.change.shopping.cart.button(),
        'clean_cart_button': i18n.clean.shopping.cart.button(),
        'items_total_price': i18n.items.total.price.text(
            total_price=float(total_price)
        ),
        'main_menu_button': i18n.main.menu.button(),
    }


async def confirmation_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    state_confirmation_text = {
        ShoppingCartSG.clean_cart_confirmation: i18n.clean.cart.text(),
        ShoppingCartSG.delete_item_confirmation: i18n.delete.item.text(),
    }
    state = dialog_manager.current_context().state

    basic_data = {
        'confirmation_text': state_confirmation_text.get(state),
        'confirm_button': i18n.yes.button(),
        'cancel_button': i18n.no.button(),
    }

    if state == ShoppingCartSG.delete_item_confirmation:
        item = dialog_manager.dialog_data.get('selected_item_data')
        basic_data.update(
            {
                'item_info': i18n.item.info.text(
                    name=item.get('name'),
                    description=item.get('description'),
                    price=item.get('price'),
                ),
                'image': item.get('image_path'),
            }
        )

    return basic_data


async def change_cart_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
):
    items, *_, = await get_shopping_cart_items(
        tg_id=event_from_user.id
    )
    item_id = dialog_manager.start_data.get('items_page_id')
    item = items[item_id]
    dialog_manager.dialog_data.update(
        {
            'selected_item_data': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'image_path': item.image.path,
                'price': float(item.price),
                'amount': item.amount,
            }
        }
    )
    return {
        'counter': i18n.counter.items(
            item_number=item_id + 1, items_amount=len(items)
        ),
        'item_info': i18n.item.info.text(
            name=item.name,
            description=item.description,
            price=float(item.price),
        ),
        'image': item.image.path,
        'back': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_item_exist': item_id + 1 < len(items),
        'previous_item_exist': item_id > 0 and len(items) > 1,
        'change_amount_button': i18n.cart.item.change.amount(),
        'cart_item_out': i18n.cart.out.button(),
        'amount_info': i18n.item.amount.cart.text(amount=item.amount),
    }


async def change_item_amount_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
):
    item_data = dialog_manager.dialog_data.get('selected_item_data')

    if 'item_amount' not in dialog_manager.start_data:
        dialog_manager.start_data['item_amount'] = item_data.get('amount')

    item_amount = dialog_manager.start_data['item_amount']

    return {
        'change_amount_text': i18n.change.item.amount.text(),
        'plus': i18n.increase.button(),
        'minus': i18n.decrease.button(),
        'item_amount': dialog_manager.start_data.get('item_amount'),
        'confirm_button': i18n.confirm.button(),
        'not_minimal': item_amount != 1,
        'cannot_decrease': item_amount == 1,
        'new_amount': item_amount != item_data.get('amount'),
        'not_new_amount': item_amount == item_data.get('amount'),
        'cancel_button': i18n.back.button(),
    }
