from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from db.requests import get_active_categories, get_active_subcategories
from dialogs import consts


async def categories_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    categories = await get_active_categories()
    cat_id = [(cat, cat) for cat in categories]
    page_id = dialog_manager.start_data.get('category_page_id')

    return {
        'categories': cat_id[
            page_id * consts.PAGE_SIZE : (page_id + 1) * consts.PAGE_SIZE
        ],
        'categories_text': i18n.category.text(),
        'main_menu': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(categories) > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0,
    }


async def subcategories_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
):
    subcategories = await get_active_subcategories(
        dialog_manager.dialog_data.get('selected_category')
    )
    subcat_id = [(subcat, subcat) for subcat in subcategories]
    page_id = dialog_manager.start_data.get('subcategory_page_id')

    return {
        'subcategories': subcat_id[
            page_id * consts.PAGE_SIZE : (page_id + 1) * consts.PAGE_SIZE
        ],
        'subcategories_text': i18n.subcategory.text(),
        'back': i18n.back.button(),
        'next': i18n.pagination.next.button(),
        'previous': i18n.pagination.previous.button(),
        'next_page_exist': len(subcategories)
        > (page_id + 1) * consts.PAGE_SIZE,
        'previous_page_exist': page_id > 0,
    }
