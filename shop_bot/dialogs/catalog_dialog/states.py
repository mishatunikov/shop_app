from aiogram.fsm.state import State, StatesGroup


class CatalogSG(StatesGroup):
    categories = State()
    subcategories = State()
    items = State()
    confirm_item_cart_add = State()
