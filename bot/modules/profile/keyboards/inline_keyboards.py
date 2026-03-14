from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PROFILE_CALL = "profile_call"
profile_button = InlineKeyboardButton(text="👤 Профиль", callback_data=PROFILE_CALL)

async def get_profile_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    from bot.modules.reputation.keyboards.inline_keyboards import REPUTATION_CALL
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="✨ Репутация", callback_data=REPUTATION_CALL)],
            [back_button]
        ]
    )
    return keyboard