from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from config import Config
from dialogs.delivery_dialog.states import DeliverySG


async def correct_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    state_data = {
        DeliverySG.name: ('name', lambda name: i18n.delivery.name(name=name)),
        DeliverySG.number: (
            'number',
            lambda number: i18n.delivery.number(number=number),
        ),
        DeliverySG.city: ('city', lambda city: i18n.delivery.city(city=city)),
        DeliverySG.street: (
            'street',
            lambda street: i18n.delivery.street(street=street),
        ),
        DeliverySG.house: (
            'house',
            lambda house: i18n.delivery.house(house=house),
        ),
        DeliverySG.flat: ('flat', lambda flat: i18n.delivery.flat(flat=flat)),
    }
    param, text_func = state_data.get(dialog_manager.current_context().state)
    delivery_data = dialog_manager.dialog_data.setdefault('delivery_data', {})
    delivery_data.update({param: message.text})

    delivery_data_messages = dialog_manager.dialog_data.get(
        'delivery_data_messages'
    )

    delivery_data_messages.append(text_func(message.text))

    await dialog_manager.next()


async def incorrect_input(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.incorrect.text.input())


async def not_text_input(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.no.text.input())


async def start_payment(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    if not dialog_manager.dialog_data.get('payment_button_pressed'):
        dialog_manager.dialog_data.update({'payment_button_pressed': True})
        prices = [
            LabeledPrice(
                label='Товар',
                amount=dialog_manager.start_data.get('total_price') * 100,
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
            need_email=False,
            need_shipping_address=True,
            is_flexible=False,
        )
        await callback.message.delete()
    else:
        await callback.answer(i18n.how.to.pay.text())
