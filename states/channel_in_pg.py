
from aiogram.dispatcher.filters.state import State, StatesGroup


class CHANNEL_IN_DB(StatesGroup):
    confirm_manager_bot = State()
    channel_name = State()
    channel_link = State()
    channel_id = State()
    description = State()
    comment = State()
    channel_theme = State()
    banned_themes = State()
    time_for_posts = State()

class FSM_CONDITIONS(StatesGroup):
    conditions = State()

    











