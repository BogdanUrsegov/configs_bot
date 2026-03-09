from aiogram import F, Router, types
from aiogram.filters import Command
from bot.database.utils import user_checker, add_user
from ..keyboards.inline_keyboards import BACK_CALL, start_menu


router = Router()


@router.callback_query(F.data == BACK_CALL)
async def profile_call(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "<b>Приветствуем!</b>\n\n"

        "<i>Конфиги для РФ — почти даром ⭐️</i>\n\n"
        "⚡ <b>Новые конфиги каждый день</b>\n"
        "📱 <b>Легкие решения для телефона и полные для ПК</b>\n"
        "🎯 <b>Автоматическая выдача</b>\n\n"
        
        "🚀 <i>Выбери действие</i> 👇",

        reply_markup=start_menu
    )