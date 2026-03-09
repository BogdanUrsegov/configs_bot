from aiogram.types import InlineKeyboardButton


INSTRUCTION_CALL = "instruction_call"
instruction_button = InlineKeyboardButton(text="📄 Инструкция", callback_data=INSTRUCTION_CALL)