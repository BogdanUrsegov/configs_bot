from sqlalchemy import update
from ..models import User
from ..session import AsyncSessionLocal

async def add_rep(telegram_id: int, amount: float) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(reputation=User.reputation + amount)
            )
            await session.commit()
            return True
    except Exception:
        return False