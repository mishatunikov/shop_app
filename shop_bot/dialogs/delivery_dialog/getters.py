from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from dialogs.delivery_dialog.states import DeliverySG


async def delivery_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):

    state_param = {
        DeliverySG.name: i18n.input.name.text(),
        DeliverySG.number: i18n.input.number.text(),
        DeliverySG.city: i18n.input.city.text(),
        DeliverySG.street: i18n.input.street.text(),
        DeliverySG.house: i18n.input.house.text(),
        DeliverySG.flat: i18n.input.flat.text(),
    }

    message = state_param.get(dialog_manager.current_context().state)
    delivery_data_messages = dialog_manager.dialog_data.setdefault(
        'delivery_data_messages', []
    )

    return {
        'text': '\n'.join(delivery_data_messages) + '\n\n' + message,
        'back_button': i18n.back.button(),
        'cancel_button': i18n.cancel.button(),
    }


async def confirmation_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
):
    delivery_data_message = dialog_manager.dialog_data.get(
        'delivery_data_messages'
    )
    return {
        'confirmation_text': i18n.confirmation.delivery.data()
        + '\n\n'
        + '\n'.join(delivery_data_message),
        'confirm_button': i18n.yes.button(),
        'cancel_button': i18n.no.button(),
    }


async def payment_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
):

    return {
        'payment_text': i18n.payment.text(),
        'payment_button': i18n.payment.button(),
        'cancel_button': i18n.cancel.button(),
        'back_button': i18n.back.button(),
    }
