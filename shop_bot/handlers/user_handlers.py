import logging

from aiogram import Bot, F, Router
from aiogram.filters import (
    KICKED,
    MEMBER,
    ChatMemberUpdatedFilter,
    CommandStart,
)
from aiogram.types import ChatMemberUpdated, Message, PreCheckoutQuery
from aiogram_dialog import DialogManager, StartMode

from db.requests import add_or_create_user, clean_shopping_cart
from dialogs.start_dialog.states import StartSG
from dialogs.utils import save_order_to_excel

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart())
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
    # To track the status in order to correctly carry out further mailing.
    logger.info(f'Пользователь id={event.from_user.id} заблокировал бота.')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def unblock_bot(event: ChatMemberUpdated):
    # To track the status in order to correctly carry out further mailing.
    logger.info(f'Пользователь id={event.from_user.id} разблокировал бота.')


@router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot
):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as err:
        logging.error(
            f"Ошибка при обработке апдейта типа PreCheckoutQuery: {err}"
        )


@router.message(F.successful_payment)
async def process_successful_payment(
    message: Message, dialog_manager: DialogManager
):
    await message.reply(
        f'Платеж на сумму {message.successful_payment.total_amount // 100} '
        f'{message.successful_payment.currency} прошел успешно!'
    )
    logging.info(f'Получен платеж от {message.from_user.id}')
    delivery_data = dialog_manager.dialog_data.get('delivery_data')
    order_data = [
        *delivery_data.values(),
        dialog_manager.start_data.get('items_amount'),
        dialog_manager.start_data.get('total_price')
    ]

    await save_order_to_excel(order_data)

    await clean_shopping_cart(tg_id=message.from_user.id)
    await dialog_manager.done()
