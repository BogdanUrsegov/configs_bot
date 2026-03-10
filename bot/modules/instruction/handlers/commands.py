from aiogram import Router, types
from aiogram.filters import Command
from bot.database.utils import user_checker, add_user
from bot.modules.constants import PRICE_WEEK

router = Router()


@router.message(Command("guide"))
async def cmd_guide(message: types.Message):
    from bot.modules.start.keyboards.inline_keyboards import back_menu
    await message.answer(
                        f"<b>🔐 Твои VLESS-конфиги за {PRICE_WEEK} Telegram Stars</b>\n\n"
                        f"Привет! 👋 За {PRICE_WEEK} Telegram Stars ты получаешь ежедневную порцию рабочих VLESS-конфигов на целую неделю. Каждый день — новый файл, всегда актуально и безопасно\n\n"
                        "<b>📦 Что ты получаешь:</b>\n"
                        "- Первый файл: 150 самых быстрых серверов, лёгкий формат 📱\n"
                        "- Второй файл: все доступные конфиги, максимум выбора 💻\n\n"
                        "📲 Подходит для клиентов:\n"
                        "<i>• 💻 ПК: v2rayN, Throne, Karing, Singbox-launcher</i>\n"
                        "<i>• 🍎 iOS: Streisand, Shadowrocket, Karing, V2Box, v2RayTun</i>\n"
                        "<i>• 🤖 Android: v2rayNG, NekoBox, V2Box</i>\n\n"

                        "<b>⚙️ Как добавить:</b>\n"
                        "1) Скопируй содержимое файла полностью 📋\n"
                        "2) В приложении выбери «Импорт из буфера» 📝\n"
                        "3) Дай имя и нажми «Обновить» ♻️\n"
                        "4) Проверь задержку — оставляй зелёные с минимальным пингом ⚡"
                                
)