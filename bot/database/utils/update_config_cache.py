import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.database.models import ConfigCache
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def update_config_cache(
    full_file_id: str, 
    mobile_file_id: str, 
    date_str: str, 
    date_ts: int
) -> bool:
    """
    Обновляет кэш конфигов только если новый timestamp свежее текущего.
    Возвращает True при успешном обновлении, False если кэш актуален или ошибка БД.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Пытаемся найти существующую запись (всегда id=1)
            stmt = select(ConfigCache).where(ConfigCache.id == 1)
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()

            if not record:
                # Если записи нет, создаем новую
                record = ConfigCache(
                    id=1,
                    full_file_id=full_file_id,
                    mobile_file_id=mobile_file_id,
                    updated_at_str=date_str,
                    updated_at_ts=date_ts
                )
                session.add(record)
                await session.commit()
                logger.info(f"✅ Создана новая запись кэша конфигов (TS: {date_ts})")
                return True
            
            # Если запись есть, сравниваем timestamp
            current_ts = record.updated_at_ts or 0
            
            if date_ts <= current_ts:
                # Новый конфиг не свежее текущего, игнорируем
                logger.info(f"⏭ Кэш актуален. Новый TS={date_ts} <= Текущий TS={current_ts}")
                return False
            
            # Новый конфиг свежее, обновляем запись
            record.full_file_id = full_file_id
            record.mobile_file_id = mobile_file_id
            record.updated_at_str = date_str
            record.updated_at_ts = date_ts
            
            await session.commit()
            logger.info(f"✅ Кэш обновлен: TS={current_ts} → TS={date_ts}")
            return True

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка БД при обновлении кэша конфигов: {e}")
            return False
        except Exception as e:
            await session.rollback()
            logger.critical(f"Критическая ошибка update_config_cache: {e}")
            raise