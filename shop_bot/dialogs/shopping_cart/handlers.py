from aiogram.types import CallbackQuery, LabeledPrice
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from config import Config
from db.requests import (
    change_item_amount,
    clean_shopping_cart,
    delete_item_from_cart,
    get_user_cart_info,
)
from dialogs.shopping_cart.states import ShoppingCartSG


async def clean_cart(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    await clean_shopping_cart(tg_id=callback.from_user.id)
    await dialog_manager.switch_to(state=ShoppingCartSG.main_page)


async def change_shopping_cart(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    dialog_manager.start_data.update({'items_page_id': 0})
    await dialog_manager.switch_to(state=ShoppingCartSG.change_cart)


async def remove_item(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    tg_id = callback.from_user.id
    item = dialog_manager.dialog_data.get('selected_item_data')
    await delete_item_from_cart(tg_id=tg_id, item_id=item.get('id'))
    if await get_user_cart_info(tg_id=tg_id):
        await dialog_manager.switch_to(state=ShoppingCartSG.change_cart)
    else:
        await dialog_manager.switch_to(state=ShoppingCartSG.main_page)


async def confirm_amount_changing(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    item_data = dialog_manager.dialog_data.get('selected_item_data')

    await change_item_amount(
        tg_id=callback.from_user.id,
        item_id=item_data.get('id'),
        amount=dialog_manager.start_data.get('item_amount'),
    )

    await dialog_manager.switch_to(ShoppingCartSG.change_cart)


async def show_confirm_alert(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.old.amount.value.text())


async def send_invoice(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    prices = [
        LabeledPrice(
            label='Товар',
            amount=dialog_manager.dialog_data.get('total_price') * 100,
        ),
    ]

    config: Config = dialog_manager.middleware_data.get('config')

    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Покупка товара',
        description='Описание товара',
        payload='test_payload',
        provider_token=config.payment.token,
        currency='RUB',
        prices=prices,
        start_parameter='test-payment',
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )
