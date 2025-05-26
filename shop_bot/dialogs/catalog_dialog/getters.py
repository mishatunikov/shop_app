from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from db.requests import (
    get_active_categories,
    get_active_subcategories,
    get_items,
)
from dialogs import consts


async def categories_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    categories = await get_active_categories()
    cat_id = [(cat, cat) for cat in categories]
    page_id = dialog_manager.start_data.get('category_page_id')

    return {
        'categories': cat_id[
            page_id * consts.PAGE_SIZE: (page_id + 1) * consts.PAGE_SIZE
        ],
        'categories_text': i18n.category.text(),
        'main_menu': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(categories) > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0 and len(categories) > 1,
    }


async def subcategories_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    subcategories = await get_active_subcategories(
        dialog_manager.dialog_data.get('selected_category')
    )
    subcat_id = [(subcat, subcat) for subcat in subcategories]
    page_id = dialog_manager.start_data.get('subcategory_page_id')

    return {
        'subcategories': subcat_id[
            page_id * consts.PAGE_SIZE: (page_id + 1) * consts.PAGE_SIZE
        ],
        'subcategories_text': i18n.subcategory.text(),
        'back': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(subcategories)
        > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0 and len(subcategories) > 1,
    }


async def items_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
):
    items = await get_items(
        subcategory_name=dialog_manager.dialog_data.get(
            'selected_subcategory'
        ),
        tg_id=event_from_user.id,
    )
    item_number = dialog_manager.start_data.get('items_page_id')
    item = items[item_number]
    dialog_manager.dialog_data['selected_item_data'] = {
        'name': item.name,
        'price': float(item.price),
        'description': item.description,
        'id': item.id,
        'image_path': item.image.path,
    }
    item_amount = dialog_manager.start_data.get('item_amount')
    return {
        'counter': i18n.counter.items(
            item_number=item_number + 1, items_amount=len(items)
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
        'next_item_exist': item_number + 1 < len(items),
        'previous_item_exist': item_number > 0 and len(items) > 1,
        'plus': i18n.increase.button(),
        'minus': i18n.decrease.button(),
        'item_amount': item_amount,
        'shopping_cart': i18n.shopping.cart.button(),
        'has_previous_item': item_amount > 1 and not item.in_cart,
        'cannot_decrease': item_amount <= 1 and not item.in_cart,
        'cart_add': i18n.cart.add.button(),
        'item_in_cart': item.in_cart,
        'not_in_cart': not item.in_cart,
        'is_added': i18n.item.added.button(),
    }


async def item_cart_add_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
):
    item_data = dialog_manager.dialog_data.get('selected_item_data')

    return {
        'item_info': i18n.item.info.text(
            name=item_data['name'],
            description=item_data['description'],
            price=item_data['price'],
        ),
        'image': item_data.get('image_path'),
        'confirm': i18n.yes.button(),
        'cancel': i18n.no.button(),
        'cart_add_answer': i18n.cart.add.confirm(
            amount=dialog_manager.start_data.get('item_amount')
        ),
    }
