import asyncio
import logging
from typing import Dict
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from bot.database.utils.get_all_users_ids import get_all_users_ids
from bot.database.session import AsyncSessionLocal
from bot.create_bot import bot

logger = logging.getLogger(__name__)

# Базовая пауза между сообщениями (секунды)
BASE_DELAY = 0.1 
# Максимальная пауза при ошибках
MAX_DELAY = 5.0 

async def broadcast() -> Dict[str, int]:
    """
    Последовательная рассылка с адаптивной задержкой.
    Безопасно для больших баз пользователей.
    """
    from bot.modules.get_access.keyboards.inline_keyboards import get_access_menu
    subscribers = await get_all_users_ids()
    total = len(subscribers)
    
    if not subscribers:
        logger.info("Нет подписчиков для рассылки.")
        return {'sent': 0, 'failed': 0, 'blocked': 0}

    logger.info(f"🚀 Запуск последовательной рассылки ({total} юзеров)...")
    
    stats = {'sent': 0, 'failed': 0, 'blocked': 0}
    current_delay = BASE_DELAY
    
    text_msg = "🔔 <b>Доступны новые конфиги!</b> 👇"

    for i, tid in enumerate(subscribers):
        try:
            await bot.send_message(
                chat_id=tid,
                text=text_msg,
                parse_mode="HTML",
                reply_markup=get_access_menu
            )
            stats['sent'] += 1
            current_delay = BASE_DELAY # Сброс задержки при успехе
            
        except TelegramForbiddenError:
            stats['blocked'] += 1
            # Юзер заблокировал бота, можно пометить в БД как неактивного (опционально)
            logger.debug(f"Юзер {tid} заблокировал бота.")
            
        except TelegramAPIError as e:
            stats['failed'] += 1
            logger.warning(f"Ошибка API для {tid}: {e}")
            # При ошибке API увеличиваем паузу, чтобы не словить FloodWait
            current_delay = min(current_delay * 2, MAX_DELAY)
            
        except Exception as e:
            stats['failed'] += 1
            logger.error(f"Неожиданная ошибка для {tid}: {e}")
            current_delay = min(current_delay * 2, MAX_DELAY)

        # Пауза между отправками
        if i < total - 1: # Не спать после последнего сообщения
            await asyncio.sleep(current_delay)
            
        # Лог прогресса каждые 100 сообщений
        if (i + 1) % 100 == 0:
            logger.info(f"Прогресс: {i+1}/{total} отправлено...")

    logger.info(f"✅ Рассылка завершена! Успешно: {stats['sent']}, Блок: {stats['blocked']}, Ошибки: {stats['failed']}")
    return stats