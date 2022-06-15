from aiogram.dispatcher.filters.state import State, StatesGroup


class CHANGE_NAME(StatesGroup):
    name = State()

class CHANGE_ID(StatesGroup):
    id = State()

class CHANGE_LINK(StatesGroup):
    link = State()

class CHANGE_description(StatesGroup):
    description = State()

class CHANGE_comment(StatesGroup):
    comment = State()

class CHANGE_banned(StatesGroup):
    banned = State()
    list = State()

class CHANGE_theme(StatesGroup):
    theme = State()

class CHANGE_price(StatesGroup):
    price = State()

class CHANGE_time(StatesGroup):
    time = State()