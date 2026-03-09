from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from bot.modules.get_access.keyboards.inline_keyboards import ONE_CONF_CALL, WEEK_SUB_CALL
from ..utils.get_conf import send_config_files


router = Router()


@router.callback_query(F.data == WEEK_SUB_CALL)
async def week_sub_call(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.message.answer("⏳ Загрузка актуальных списков...")
    
    success = await send_config_files(callback.bot, user_id)
    
    if not success:
        await callback.message.answer("⚠️ Произошла ошибка при получении данных.")

