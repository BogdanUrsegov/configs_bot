from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

WEEK_SUB_CALL = "week_sub_call"
ONE_CONF_CALL = "one_conf_call"
GET_ACCESS_CALL = "get_access_call"


get_access_button = InlineKeyboardButton(text="📲 Получить", callback_data=GET_ACCESS_CALL)

get_access_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [get_access_button]
    ]
)
