from aiogram.dispatcher.filters.state import State, StatesGroup


class QIWI_P2P_REQV(StatesGroup):
    token = State()