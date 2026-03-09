from typing import Optional
from sqlalchemy import Integer, DateTime, BigInteger, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

# Базовый класс для асинхронных моделей
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Дата подписки: nullable=True, если подписка не обязательна сразу
    subscription_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )


class ConfigCache(Base):
    __tablename__ = "config_cache"

    # Первичный ключ (всегда 1 запись)
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    
    # File IDs от Telegram
    full_file_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mobile_file_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Время обновления: строка и timestamp (секунды)
    updated_at_str: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at_ts: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    def __repr__(self) -> str:
        return f"<ConfigCache(full={self.full_file_id}, mobile={self.mobile_file_id}, ts={self.updated_at_ts})>"