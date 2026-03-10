from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards.inline_keyboards import PROFILE_CALL
from bot.database.utils.get_subscription_status import get_subscription_status


router = Router()

@router.callback_query(F.data == PROFILE_CALL)
async def profile_call(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    # Получаем словарь со статусом и датой
    data = await get_subscription_status(user_id)
    status = data["status"]
    date_info = data["date"] if data["date"] else "-"

    await callback.answer()

    from bot.modules.start.keyboards.inline_keyboards import back_menu
    await callback.message.edit_text(
        f"<b>👤 Профиль</b>\n\n"
        f"<b>💎 Статус:</b> {status}\n"
        f"<b>🕒 Действует до:</b> {date_info}",
        reply_markup=back_menu
    )