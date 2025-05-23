from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from db.requests import get_categories
from dialogs import consts


async def categories_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    categories = dialog_manager.dialog_data.get(
        'categories',
    )
    if not categories:
        categories = await get_categories()
        dialog_manager.dialog_data.update({'categories': categories})

    cat_id = [(cat, num) for num, cat in enumerate(categories)]
    page_id = dialog_manager.start_data.get('page_id')

    return {
        'categories': cat_id[
            page_id * consts.PAGE_SIZE: (page_id + 1) * consts.PAGE_SIZE
        ],
        'categories_text': i18n.category.text(),
        'main_menu': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(categories) > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0,
    }
