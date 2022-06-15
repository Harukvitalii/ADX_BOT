from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMPAYQIWI(StatesGroup):
    qiwi = State()
    deposit = State()
    # ym = State()


class FSMPAYWM(StatesGroup):
    wm = State()
    deposit = State()
    # ym = State()


class FSMPAYYM(StatesGroup):
    YM = State()
    deposit = State()

class FSMBTC_BANKER(StatesGroup):
    btc_banker = State()
    check = State()
    deposit = State()
