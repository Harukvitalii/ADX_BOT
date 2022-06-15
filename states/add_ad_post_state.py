from aiogram.dispatcher.filters.state import State, StatesGroup


class AD_POST(StatesGroup):
    
    name = State()
    post = State()
    kb = State()


