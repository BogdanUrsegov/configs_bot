import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.database.models import ConfigCache
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def get_config_cache() -> Optional[ConfigCache]:
    """
    Возвращает запись с кэшем конфигов (id=1).
    Если записи нет или произошла ошибка БД, возвращает None.
    """
    async with AsyncSessionLocal() as session:
        try:
            stmt = select(ConfigCache).where(ConfigCache.id == 1)
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            
            if record:
                logger.debug(f"Кэш конфигов найден: TS={record.updated_at_ts}")
            else:
                logger.warning("Запись кэша конфигов не найдена в БД")
            
            return record

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка БД при получении кэша конфигов: {e}")
            return None
        except Exception as e:
            await session.rollback()
            logger.critical(f"Критическая ошибка get_config_cache: {e}")
            return None