# bot/database/session.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from urllib.parse import urlparse
from .models import Base
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db")

# Парсим URL для получения имени файла (опционально, если нужно логировать)
parsed_url = urlparse(DATABASE_URL)
db_name = parsed_url.path.lstrip('/')

if not db_name:
    logger.warning("Не удалось определить имя базы данных, используется дефолтное.")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def init_db():
    """Создаёт таблицы, если их нет."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f"Таблицы успешно созданы/обновлены в {db_name}")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise