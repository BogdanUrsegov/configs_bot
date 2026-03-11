from datetime import datetime, timezone
from aiogram import F, Bot, Router, types
from aiogram.fsm.context import FSMContext
from bot.database.utils.get_config_cache import get_config_cache
import logging
from bot.modules.constants import PRICE_WEEK

from bot.database.utils.is_subscription_active import is_subscription_active
from bot.scheduler.tasks.get_configs import send_and_save_configs
from ..keyboards.inline_keyboards import GET_ACCESS_CALL
from bot.modules.buy_sub.keyboards.inline_keyboards import get_buy_sub_menu


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == GET_ACCESS_CALL)
async def get_access_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id

    if not await is_subscription_active(user_id):
        await callback.answer("⛔️ Отсутствует подписка")
        await callback.message.edit_text(
                                    f"<b>🔐 VLESS конфиги — {PRICE_WEEK} Stars на неделю</b>\n\n"
                                    f"✅ Ежедневно: Под телефон + Все проверенные\n"
                                    f"📱 <b>PC, iOS, Android</b> (v2rayN, Streisand, V2Box и тд)\n"
                                    f"⚙️ <b>Установка:</b> Копируй → Импорт из буфера → Обновить\n\n"
                                    f"<b>🚀 Жми кнопку для доступа!</b>"
                                    , 
                                    reply_markup=get_buy_sub_menu()
    )
    else:
        await callback.answer("⏳ Загрузка актуальных списков...")
        record = await get_config_cache()
        
        if record and record.full_file_id and record.mobile_file_id:
            # ✅ Кэш найден: отправляем файлы по ID мгновенно
            logger.info(f"Отправка конфигов из кэша (TS: {record.updated_at_ts})")
            
            # Формируем читаемую дату из timestamp для подписи
            if record.updated_at_ts:
                dt = datetime.fromtimestamp(record.updated_at_ts, tz=timezone.utc)
                date_str = dt.strftime("%d.%m.%Y %H:%M")
            else:
                date_str = "Неизвестно"
                
            caption = f"🕒 Обновлено: {date_str} UTC"
            
            try:
                await bot.send_media_group(
                    chat_id=user_id,
                    media=[
                        types.InputMediaDocument(media=record.full_file_id),
                        types.InputMediaDocument(media=record.mobile_file_id, caption=caption)
                    ]
                )
            except Exception as e:
                logger.error(f"Ошибка отправки из кэша (возможно, файл удален): {e}")
                # Если файл удален телеграмом (ошибка 400), нужно перегенерировать
                await callback.message.answer("⚠️ Файлов нет или они повреждены. Загружаю новые файлы...")
                await send_and_save_configs(user_id)
                
        else:
            # ❌ Кэша нет: скачиваем, отправляем и сохраняем в БД
            logger.warning("Кэш конфигов пуст. Запуск полной загрузки.")
            await callback.message.answer("⏳ Файлов нет. Скачиваю актуальные списки...")
            await send_and_save_configs(user_id)