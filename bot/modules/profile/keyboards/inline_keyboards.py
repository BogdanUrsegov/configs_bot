from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PROFILE_CALL = "profile_call"
REPUTATION_CALL = "reputation_call"
VIEW_ADS_CALL = "view_ads_call"
INVITE_FRIENDS_CALL = "invite_friends_call"
GET_FREE_ACCESS_CALL = "get_free_access_call"
profile_button = InlineKeyboardButton(text="👤 Профиль", callback_data=PROFILE_CALL)

async def get_profile_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="✨ Репутация", callback_data=REPUTATION_CALL)],
            [back_button]
        ]
    )
    return keyboard

async def get_reputation_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="Смотреть рекламу 📺", callback_data=VIEW_ADS_CALL), InlineKeyboardButton(text="Пригласить друзей 🗣", callback_data=INVITE_FRIENDS_CALL)],
            [InlineKeyboardButton(text="Получить доступ ⭐️", callback_data=GET_FREE_ACCESS_CALL)],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=PROFILE_CALL)]
        ]
    )
    return keyboard

async def get_invite_friends_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=REPUTATION_CALL)]
        ]
    )
    return keyboard

async def view_ads_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=REPUTATION_CALL)]
        ]
    )
    return keyboard