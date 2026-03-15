from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F

from bot.database.utils.get_user_reputation import get_user_reputation
from bot.modules.constants import CONF_FOR_REP
from bot.modules.reputation.keyboards.inline_keyboards import get_reputation_menu


router = Router()

@router.message(CommandStart(), F.args == "reputation")
async def start_reputation(message: Message):
    user_id = message.from_user.id
    reputation = await get_user_reputation(user_id)

    await message.answer(
        f"<b>✨ Ваша репутация:</b> {reputation:.1f}\n\n"
        "📊 Это показатель вашей активности в боте\n\n"
        f"🎁 <b>Обмен:</b> {CONF_FOR_REP} очков репутации за недельную подписку к конфигам!\n"
        "🚀 <b>Как поднять:</b> приглашение друзей и оплата платной подписки…",
        reply_markup=await get_reputation_menu()
    )