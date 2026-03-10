from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUY_SUB_CALL = "buy_sub_call"

def get_buy_sub_menu() -> InlineKeyboardMarkup:
    from bot.modules.start.keyboards.inline_keyboards import back_button
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [back_button, InlineKeyboardButton(text="📖 Инструкция", url="https://telegra.ph/Instrukciya-03-10-22")],
            [InlineKeyboardButton(text="⭐️ Приобрести подписку", callback_data=BUY_SUB_CALL)]
        ]
    )