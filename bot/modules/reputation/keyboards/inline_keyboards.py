from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


REPUTATION_CALL = "reputation_call"
INVITE_FRIENDS_CALL = "invite_friends_call"
GET_FREE_ACCESS_CALL = "get_free_access_call"


async def get_reputation_menu():
    from bot.modules.start.keyboards.inline_keyboards import back_button
    from bot.modules.profile.keyboards.inline_keyboards import PROFILE_CALL
    from bot.modules.get_access.keyboards.inline_keyboards import GET_ACCESS_CALL

    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="Купить подписку 💳", callback_data=GET_ACCESS_CALL)],
            [InlineKeyboardButton(text="Пригласить друзей 🗣", callback_data=INVITE_FRIENDS_CALL)],
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