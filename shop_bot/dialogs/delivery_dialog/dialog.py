from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next
from aiogram_dialog.widgets.text import Format

from dialogs.delivery_dialog.filters import (
    IsAlpha,
    IsNumber,
    IsNumberOrNotExist,
    IsPhoneNumber,
)
from dialogs.delivery_dialog.getters import (
    confirmation_getter,
    delivery_getter,
    payment_getter,
)
from dialogs.delivery_dialog.handlers import (
    correct_input,
    incorrect_input,
    not_text_input,
    start_payment,
)
from dialogs.delivery_dialog.states import DeliverySG
from dialogs.general_handlers import back

delivery_dialog = Dialog(
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsAlpha(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Cancel(Format('{back_button}')),
        state=DeliverySG.name,
        getter=delivery_getter,
    ),
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsPhoneNumber(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Button(Format('{back_button}'), id='number_input_back', on_click=back),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.number,
        getter=delivery_getter,
    ),
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsAlpha(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Button(Format('{back_button}'), id='city_input_back', on_click=back),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.city,
        getter=delivery_getter,
    ),
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsAlpha(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Button(Format('{back_button}'), id='street_input_back', on_click=back),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.street,
        getter=delivery_getter,
    ),
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsNumber(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Button(Format('{back_button}'), id='house_input_back', on_click=back),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.house,
        getter=delivery_getter,
    ),
    Window(
        Format('{text}'),
        MessageInput(
            func=correct_input,
            content_types=ContentType.TEXT,
            filter=IsNumberOrNotExist(),
        ),
        MessageInput(func=incorrect_input, content_types=ContentType.TEXT),
        MessageInput(func=not_text_input, content_types=ContentType.ANY),
        Button(Format('{back_button}'), id='flat_input_back', on_click=back),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.flat,
        getter=delivery_getter,
    ),
    Window(
        Format('{confirmation_text}'),
        Next(
            Format('{confirm_button}'),
        ),
        Back(Format('{cancel_button}')),
        state=DeliverySG.confirmation_delivery_data,
        getter=confirmation_getter,
    ),
    Window(
        Format('{payment_text}'),
        Button(
            Format('{payment_button}'),
            id='payment',
            on_click=start_payment,
        ),
        Back(Format('{back_button}')),
        Cancel(Format('{cancel_button}')),
        state=DeliverySG.payment,
        getter=payment_getter,
    ),
)
