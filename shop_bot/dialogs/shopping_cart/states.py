from aiogram.fsm.state import State, StatesGroup


class ShoppingCartSG(StatesGroup):
    main_page = State()
    make_order = State()
    clean_cart_confirmation = State()
    change_cart = State()
    delete_item_confirmation = State()
    change_item_count = State()
