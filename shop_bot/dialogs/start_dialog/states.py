from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    main_menu = State()
    faq = State()
