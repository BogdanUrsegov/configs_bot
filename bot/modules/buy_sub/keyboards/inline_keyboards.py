from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUY_SUB_CALL = "buy_sub_call"

buy_sub_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⭐️ Приобрести подписку", callback_data=BUY_SUB_CALL)]
    ]
)