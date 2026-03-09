import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def set_subscription_week(telegram_id: int) -> bool:
    """Устанавливает дату подписки: текущее время + 7 дней. Возвращает True при успехе."""
    async with AsyncSessionLocal() as session:
        try:
            # Ищем пользователя
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()

            if not user:
                logger.warning(f"Пользователь {telegram_id} не найден для обновления подписки")
                return False

            # Вычисляем дату: Москва (или UTC) + 7 дней
            # Используем timezone-aware datetime для корректности
            now = datetime.now(timezone.utc) 
            user.subscription_date = now + timedelta(days=7)

            await session.commit()
            logger.info(f"Подписка для {telegram_id} продлена до {user.subscription_date}")
            return True

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка БД при обновлении подписки {telegram_id}: {e}")
            return False
        except Exception as e:
            await session.rollback()
            logger.error(f"Критическая ошибка set_subscription_week: {e}")
            raise