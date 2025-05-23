from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def change_page(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    **kwargs,
):
    widget_offset = {'next_page': 1, 'previous_page': -1}
    dialog_manager.start_data['page_id'] += widget_offset[widget.widget_id]
