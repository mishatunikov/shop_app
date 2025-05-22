import logging

from aiogram.filters import (
    CommandStart,
    ChatMemberUpdatedFilter,
    KICKED,
    MEMBER,
)
from aiogram.types import Message, ChatMemberUpdated
from aiogram import Router

router = Router()


logger = logging.getLogger(__name__)


@router.message(CommandStart)
def start(message: Message):
    logger.info(f'Пользователь id={message.from_user.id} активировал бота.')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def block_bot(event: ChatMemberUpdated):
    logger.info(f'{event.new_chat_member.status}')
    logger.info(f'Пользователь id={event.from_user.id} заблокировал бота.')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def unblock_bot(event: ChatMemberUpdated):
    logger.info(f'Пользователь id={event.from_user.id} разблокировал бота.')
