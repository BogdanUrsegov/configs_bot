import logging
from sqlalchemy.exc import IntegrityError
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def add_user(telegram_id: int) -> bool:
    """Добавляет пользователя. Возвращает True при успехе, False если ID занят."""
    async with AsyncSessionLocal() as session:
        try:
            new_user = User(telegram_id=telegram_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"Пользователь {telegram_id} успешно добавлен")
            return True
        except IntegrityError:
            # Ошибка уникальности (ID уже существует)
            await session.rollback()
            logger.warning(f"Пользователь {telegram_id} уже существует")
            return False
        except Exception as e:
            await session.rollback()
            logger.error(f"Критическая ошибка add_user: {e}")
            raise  # Перевыбрасываем только критические ошибки