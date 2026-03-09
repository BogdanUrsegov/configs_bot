from datetime import datetime, timezone
from aiogram import F, Bot, Router, types
from aiogram.fsm.context import FSMContext
from bot.database.utils.get_config_cache import get_config_cache
import logging
from bot.modules.constants import PRICE_WEEK

from bot.database.utils.is_subscription_active import is_subscription_active
from bot.scheduler.tasks.get_configs import send_and_save_configs
from ..keyboards.inline_keyboards import get_access_menu
from ..keyboards.inline_keyboards import GET_ACCESS_CALL, WEEK_SUB_CALL
from bot.modules.buy_sub.keyboards.inline_keyboards import buy_sub_menu


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == GET_ACCESS_CALL)
async def get_access_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id

    if not await is_subscription_active(user_id):
        await callback.answer("⛔️ Отсутствует подписка")
        await callback.message.answer(
                                    f"<b>🔐 VLESS конфиги — {PRICE_WEEK} Stars на неделю</b>\n\n"
                                    f"✅ Ежедневно: Под телефон + Все проверенные\n"
                                    f"📱 <b>PC, iOS, Android</b> (v2rayN, Streisand, V2Box и тд)\n"
                                    f"⚙️ <b>Установка:</b> Копируй → Импорт из буфера → Обновить\n\n"
                                    f"/guide — <b>Подробная инструкция</b>\n\n"
                                    f"<b>🚀 Жми кнопку для доступа!</b>"
                                    , 
                                    reply_markup=buy_sub_menu
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
                
            caption = f"конфиги:\n🕒 Обновлено: {date_str}"
            
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
                await callback.message.answer("⚠️ Кэш устарел или поврежден. Загружаю новые файлы...")
                await send_and_save_configs(user_id)
                
        else:
            # ❌ Кэша нет: скачиваем, отправляем и сохраняем в БД
            logger.warning("Кэш конфигов пуст. Запуск полной загрузки.")
            await callback.message.answer("⏳ Кэш пуст. Скачиваю актуальные списки с GitHub...")
            await send_and_save_configs(user_id)

    
@router.callback_query(F.data == WEEK_SUB_CALL)
async def week_sub_call(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if await is_subscription_active(user_id):
        await callback.answer("⛔️ Отсутствует подписка")
        await callback.message.answer("ℹ️ <b>Нужно приобрести подписку, чтобы начать получать свежие конфиги каждый день!</b>", reply_markup=buy_sub_menu)
    else:
        await callback.message.answer("⏳ Загрузка актуальных списков...")
    
        success = await send_and_save_configs(user_id)
        
        if not success:
            await callback.message.answer("⚠️ Произошла ошибка при получении данных.")

