import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def is_subscription_active(telegram_id: int) -> bool:
    """
    Проверяет активность подписки.
    Возвращает True, если подписка действительна (дата > сейчас).
    Возвращает False, если подписки нет или она истекла.
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User.subscription_date).where(User.telegram_id == telegram_id))
            sub_date = result.scalar_one_or_none()

            # Если даты нет — подписки нет
            if sub_date is None:
                return False

            # Сравниваем с текущим UTC временем
            # Подписка активна, если дата окончания больше текущего момента
            now = datetime.now(timezone.utc)
            
            # Убедимся, что сравниваем объекты с одинаковой информаций о таймзоне
            if sub_date.tzinfo is None:
                # Если в БД время без зоны (legacy), считаем его UTC для сравнения
                # Но лучше хранить всё с timezone=True
                return sub_date.replace(tzinfo=timezone.utc) > now
            
            is_active = sub_date > now
            
            if not is_active:
                logger.debug(f"Подписка пользователя {telegram_id} истекла ({sub_date})")
            
            return is_active

        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при проверке подписки {telegram_id}: {e}")
            # При ошибке БД безопаснее вернуть False (доступ закрыт) или raise, зависит от логики
            return False
        except Exception as e:
            logger.error(f"Критическая ошибка is_subscription_active: {e}")
            raise