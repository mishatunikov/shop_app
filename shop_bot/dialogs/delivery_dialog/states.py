from aiogram.fsm.state import State, StatesGroup


class DeliverySG(StatesGroup):
    name = State()
    number = State()
    city = State()
    street = State()
    house = State()
    flat = State()
    confirmation_delivery_data = State()
    payment = State()

