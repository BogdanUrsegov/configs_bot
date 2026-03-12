from aiogram import Router, types, Bot
from aiogram.filters import Command
from bot.database.utils import user_checker, add_user
from bot.database.utils.add_rep import add_rep
from bot.modules.constants import REP_FOR_USER
from ..keyboards.inline_keyboards import start_menu


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    await message.answer(
        "<b>Приветствуем!</b>\n\n"

        "<i>Конфиги для РФ — почти даром ⭐️</i>\n\n"
        "⚡ <b>Новые конфиги каждый день</b>\n"
        "📱 <b>Легкие решения для телефона и полные для ПК</b>\n"
        "🎯 <b>Автоматическая выдача</b>\n\n"
        
        "🚀 <i>Выбери действие</i> 👇",

        reply_markup=start_menu
    )
        
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь
    is_user = await user_checker(telegram_id)

    if not is_user:
        # Создаём нового пользователя
        referrer_id = None
        # теперь получаем из параметра старт реферрер ид
        referrer_id = int(message.text.split()[1]) if len(message.text.split()) > 1 and message.text.split()[1].isdigit() else None
        await add_user(telegram_id)
        res = await add_rep(referrer_id, REP_FOR_USER)
        if res and referrer_id:
            await bot.send_message(referrer_id, f"<b>🎉 Вы получили {REP_FOR_USER} очков репутации за приглашение друга!</b>")

@router.message(Command("delete_me"))
async def cmd_delete_me(message: types.Message, bot: Bot):
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь
    is_user = await user_checker(telegram_id)

    if is_user:
        from bot.database.utils.del_user import del_user
        await del_user(telegram_id)
        await message.answer("Ваш аккаунт удалён. Если хотите вернуться, просто отправьте /start.")