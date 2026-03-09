import logging
from datetime import datetime, timezone
from sqlalchemy import select
from bot.database.models import User
from bot.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

async def get_subscription_status(telegram_id: int) -> dict:
    """
    Возвращает словарь:
    - 'status': 'Активна' или 'Неактивна'
    - 'date': строка с датой (UTC) или None
    """
    async with AsyncSessionLocal() as session:
        try:
            query = select(User.subscription_date).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            sub_date = result.scalar_one_or_none()

            now_utc = datetime.now(timezone.utc)
            
            if sub_date:
                # Если дата в БД без часового пояса, принудительно считаем её UTC
                if sub_date.tzinfo is None:
                    sub_date = sub_date.replace(tzinfo=timezone.utc)
                
                # Теперь сравнение корректно
                if sub_date >= now_utc:
                    date_str = sub_date.strftime("%Y-%m-%d %H:%M:%S")
                    return {"status": "Активна", "date": f"{date_str} (UTC)"}
            
            return {"status": "Неактивна", "date": None}

        except Exception as e:
            logger.error(f"Ошибка статуса подписки {telegram_id}: {e}")
            raise