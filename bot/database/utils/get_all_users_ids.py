import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def get_all_users_ids() -> List[int]:
    """
    Возвращает список только с telegram_id всех пользователей.
    Максимально эффективно: не загружает объекты моделей, только числа.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Выбираем строго один столбец telegram_id
            stmt = select(User.telegram_id)
            result = await session.execute(stmt)
            
            # .scalars() превращает строки результата в простые значения (int)
            user_ids = list(result.scalars().all())
            
            logger.info(f"Получено {len(user_ids)} ID пользователей")
            return user_ids

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка БД при получении ID пользователей: {e}")
            return []
        except Exception as e:
            await session.rollback()
            logger.critical(f"Критическая ошибка get_all_users_ids: {e}")
            return []