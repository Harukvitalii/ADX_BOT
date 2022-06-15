from aiogram.utils.callback_data import CallbackData




theme_callback = CallbackData("theme", 'theme_name')

my_channels_callback = CallbackData('change_chnl', "lvl", "channel_id", "row")

banned_theme_callback = CallbackData("banned", 'theme_name')