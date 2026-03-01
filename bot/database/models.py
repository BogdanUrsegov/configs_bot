from sqlalchemy import Integer, DateTime, BigInteger, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

# Базовый класс для асинхронных моделей
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )