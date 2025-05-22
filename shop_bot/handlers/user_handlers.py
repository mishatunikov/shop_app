import logging

from aiogram import Router
from aiogram.filters import (
    KICKED,
    MEMBER,
    ChatMemberUpdatedFilter,
    CommandStart,
)
from aiogram.types import ChatMemberUpdated, Message
from aiogram_dialog import DialogManager, StartMode

from db.requests import add_or_create_user
from dialogs.start_dialog.states import StartSG

router = Router()


logger = logging.getLogger(__name__)


@router.message(CommandStart)
async def start(message: Message, dialog_manager: DialogManager):
    logger.info(f'Пользователь id={message.from_user.id} активировал бота.')
    await add_or_create_user(
        message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    await dialog_manager.start(
        state=StartSG.main_menu,
        mode=StartMode.RESET_STACK,
        data={'first_open': True},
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def block_bot(event: ChatMemberUpdated):
    logger.info(f'Пользователь id={event.from_user.id} заблокировал бота.')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def unblock_bot(event: ChatMemberUpdated):
    logger.info(f'Пользователь id={event.from_user.id} разблокировал бота.')
