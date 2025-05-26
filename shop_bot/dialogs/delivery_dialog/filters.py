import re
from string import digits

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager

from dialogs.delivery_dialog.states import DeliverySG


class IsAlpha(BaseFilter):

    async def __call__(self, message: Message, dialog_manager: DialogManager):

        state = dialog_manager.current_context().state

        if state == DeliverySG.city and '-' in message.text:
            text = message.text.split('-')
        else:
            text = message.text.split()

        if not ''.join(text).isalpha():
            return False

        return True


class IsNumber(BaseFilter):

    async def __call__(self, message: Message):

        if not re.fullmatch(r'[1-9]\d*', message.text):
            return False

        return True


class IsNumberOrNotExist(IsNumber):

    async def __call__(self, message: Message, dialog_manager: DialogManager):
        if (
            dialog_manager.current_context().state == DeliverySG.flat
            and message.text == '-'
        ):
            return True

        return super().__call__(message)


class IsPhoneNumber(BaseFilter):

    async def __call__(self, message: Message):

        if not re.fullmatch(r'7\d{10}', message.text):
            return False

        return True
