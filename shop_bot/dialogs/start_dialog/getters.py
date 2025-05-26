from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from db.requests import get_faq
from dialogs import consts


async def main_menu_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    i18n: TranslatorRunner,
    **kwargs,
):
    text_selection = int(dialog_manager.start_data.get('first_open'))

    if dialog_manager.start_data.get('first_open'):
        dialog_manager.start_data['first_open'] = False

    return {
        'main_menu_text': i18n.main.menu.text(
            text_selection=text_selection, name=event_from_user.first_name
        ),
        'catalog_button': i18n.catalog.button(),
        'shopping_cart_button': i18n.shopping.cart.button(),
        'faq_button': i18n.faq.button(),
    }


async def faq_getter(
    i18n: TranslatorRunner, dialog_manager: DialogManager, **kwargs
):
    questions, exist = await get_faq()

    question_id = [(question, question) for question in questions]
    page_id = dialog_manager.start_data.get('faq_page_id')

    return {
        'faq_text': i18n.faq.text(),
        'main_menu_button': i18n.main.menu.button(),
        'exist': exist,
        'questions': question_id[
            page_id * consts.PAGE_SIZE: (page_id + 1) * consts.PAGE_SIZE
        ],
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(questions) > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0 and len(questions) > 1,
    }


'''    return {
        'categories': cat_id[
            page_id * consts.PAGE_SIZE: (page_id + 1) * consts.PAGE_SIZE
        ],
        'categories_text': i18n.category.text(),
        'main_menu': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(categories) > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0 and len(categories) > 1,
    }'''
