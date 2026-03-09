from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PROFILE_CALL = "profile_call"
profile_button = InlineKeyboardButton(text="👤 Профиль", callback_data=PROFILE_CALL)