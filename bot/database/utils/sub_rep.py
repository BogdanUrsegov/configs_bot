from sqlalchemy import update

from ..models import User
from ..session import AsyncSessionLocal

async def sub_rep(telegram_id: int, amount: float) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .where(User.reputation >= amount)
                .values(reputation=User.reputation - amount)
            )
            await session.commit()
            return result.rowcount > 0
    except Exception:
        return False