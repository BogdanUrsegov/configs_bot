import logging
from sqlalchemy import select
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def user_checker(telegram_id: int) -> bool:
    """Проверяет существование пользователя. Возвращает True/False."""
    async with AsyncSessionLocal() as session:
        try:
            # Выбираем ID для проверки существования
            query = select(User.id).where(User.telegram_id == telegram_id).limit(1)
            result = await session.execute(query)
            
            # scalar_one_or_none вернет значение или None
            return result.scalar_one_or_none() is not None
            
        except Exception as e:
            logger.error(f"Ошибка проверки пользователя {telegram_id}: {e}")
            # При критической ошибке БД лучше вернуть False или выбросить исключение
            # В зависимости от того, хотите ли вы прерывать выполнение бота
            raise 