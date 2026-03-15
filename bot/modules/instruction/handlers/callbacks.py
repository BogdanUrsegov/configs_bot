from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from bot.modules.constants import PRICE_WEEK
from ..keyboards.inline_keyboards import INSTRUCTION_CALL


router = Router()


@router.callback_query(F.data == INSTRUCTION_CALL)
async def instruction_call(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    from bot.modules.start.keyboards.inline_keyboards import back_menu
    await callback.message.edit_text(
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
                                "3) Нажми «Обновить» и пропингуй ♻️\n"
                                "4) Проверь задержку — оставляй зелёные с минимальным пингом ⚡\n\n"
                                
                                "<i>В зависимости от клиента настройка может чуть отличаться</i>",
                                reply_markup=back_menu
                                
)