from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext

from bot.database.utils.sub_rep import sub_rep
from bot.database.utils.set_subscription_week import set_subscription_week
from ..keyboards.inline_keyboards import (
    GET_FREE_ACCESS_CALL, PROFILE_CALL, REPUTATION_CALL, 
    VIEW_ADS_CALL, INVITE_FRIENDS_CALL, 
    get_profile_menu, get_reputation_menu,
    get_invite_friends_menu, view_ads_menu
)
from bot.database.utils.get_subscription_status import get_subscription_status
from bot.database.utils.get_user_reputation import get_user_reputation
from bot.modules.constants import CONF_FOR_REP, REP_FOR_USER


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

@router.callback_query(F.data == REPUTATION_CALL)
async def reputation_call(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    reputation = await get_user_reputation(user_id)

    await callback.answer()

    await callback.message.edit_text(
        f"<b>✨ Ваша репутация:</b> {reputation:.1f}\n\n"
        "📊 Это показатель вашей активности в боте\n\n"
        f"🎁 <b>Обмен:</b> {CONF_FOR_REP} очков репутации за недельную подписку к конфигам!\n"
        "🚀 <b>Как поднять:</b> приглашение друзей и просмотр рекламы…",
        reply_markup=await get_reputation_menu()
    )

@router.callback_query(F.data == INVITE_FRIENDS_CALL)
async def invite_friends_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    name_bot = (await bot.get_me()).username
    await callback.message.edit_text(
        "🔗 <b>Пригласите друзей и получите репутацию!</b>\n\n"
        f"✅ За каждого приглашенного друга, который начнет использовать бота, вы получите {REP_FOR_USER} очков репутации\n\n"
        "📌 <i>Поделитесь своей реферальной ссылкой:</i>\n"
        f"<i>https://t.me/{name_bot}?start={callback.from_user.id}</i>",
        reply_markup=await get_invite_friends_menu()
    )

@router.callback_query(F.data == VIEW_ADS_CALL)
async def view_ads_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup()
    await callback.message.answer("🔉 <i>Реклама закончилась. Приходите позже!</i>", reply_markup=await view_ads_menu())

@router.callback_query(F.data == GET_FREE_ACCESS_CALL)
async def get_free_access_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    res = await sub_rep(user_id, CONF_FOR_REP)
    if res:
        await callback.answer("✅ Вы обменяли репутацию на недельную подписку!")
        user_id = callback.from_user.id
        await set_subscription_week(user_id)
        from bot.modules.start.keyboards.inline_keyboards import back_menu
        await callback.message.answer(
            "✅ <b>Вы успешно обменяли репутацию на недельную подписку!</b>\n\n"
                            
            "📲 <i>Вернитесь обратно и нажмите кнопку для получения свежих конфигураций</i>",
            reply_markup=back_menu
        )
    else:
        await callback.answer("⚠️ У вас недостаточно репутации для обмена")