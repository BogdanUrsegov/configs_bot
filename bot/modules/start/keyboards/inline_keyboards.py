from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.modules.instruction.keyboards.inline_keyboards import instruction_button
from bot.modules.get_access.keyboards.inline_keyboards import get_access_button
from bot.modules.profile.keyboards.inline_keyboards import profile_button


BACK_CALL = "back_call"


start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [get_access_button],
        [instruction_button],
        [profile_button]

    ]
)

back_button = InlineKeyboardButton(text="🔙 Назад", callback_data=BACK_CALL)
back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [back_button]
    ]
)