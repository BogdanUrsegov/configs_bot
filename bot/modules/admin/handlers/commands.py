import os
from aiogram import Router, types
from aiogram.filters import Command
from bot.database.utils.get_users_stats import get_users_stats

router = Router()


ADMIN_ID = int(os.getenv("ADMIN_ID"))


@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer(
            "/stats - получить статистику пользователей"
            )

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    
    stats = await get_users_stats()
    
    # Формируем строку роста по дням
    growth_text = "\n".join(
        f"• {d['date']}: <b>{d['count']}</b>" 
        for d in stats["weekly_growth"]
    )

    text = (
        "📊 <b>Статистика бота</b>\n\n"
        f"👥 Всего пользователей: <b>{stats['total']}</b>\n"
        f"💎 Активных подписок: <b>{stats['active_subscriptions']}</b>\n\n"
        f"📈 <b>Прирост за 7 дней:</b>\n{growth_text}"
    )

    await message.answer(text)