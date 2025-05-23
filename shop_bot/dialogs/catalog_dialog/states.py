from aiogram.fsm.state import State, StatesGroup


class CatalogSG(StatesGroup):
    categories = State()
    subcategories = State()
    items = State()
