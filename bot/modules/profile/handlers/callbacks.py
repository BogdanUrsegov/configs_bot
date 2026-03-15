from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from bot.database.utils.add_rep import add_rep
from bot.gramads.gramads import show_advert
from ..keyboards.inline_keyboards import PROFILE_CALL, get_profile_menu
from bot.database.utils.get_subscription_status import get_subscription_status
from bot.database.utils.get_user_reputation import get_user_reputation
from bot.database.utils.sub_rep import sub_rep
from bot.modules.constants import CONF_FOR_REP, REP_FOR_USER
import logging


logger = logging.getLogger(__name__)


router = Router()

@router.callback_query(F.data == PROFILE_CALL)
async def profile_call(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    # Получаем словарь со статусом и датой
    data = await get_subscription_status(user_id)
    status = data["status"]
    date_info = data["date"] if data["date"] else "-"
    reputation = await get_user_reputation(user_id)

    await callback.answer()

    await callback.message.edit_text(
        f"<b>👤 Профиль</b>\n\n"
        f"<b>⭐ Репутация:</b> {reputation:.1f}\n\n"
        f"<b>💎 Статус подписки:</b> {status}\n"
        f"<b>🕒 Действует до:</b> {date_info}",
        reply_markup=await get_profile_menu()
    )