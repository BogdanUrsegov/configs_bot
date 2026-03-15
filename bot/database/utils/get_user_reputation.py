from sqlalchemy import select
from bot.database.models import User
from bot.database.session import AsyncSessionLocal
import logging


logger = logging.getLogger(__name__)

async def get_user_reputation(telegram_id: int) -> float:
    async with AsyncSessionLocal() as session:
        query = select(User.reputation).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        reputation = result.scalar_one_or_none()
        logger.info(f"Reputation for user {telegram_id}: {reputation}")
        return reputation if reputation is not None else 0.0