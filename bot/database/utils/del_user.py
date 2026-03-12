from sqlalchemy import delete

from ..models import User

from ..session import AsyncSessionLocal

async def del_user(telegram_id: int) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                delete(User).where(User.telegram_id == telegram_id)
            )
            await session.commit()
            return result.rowcount > 0
    except Exception:
        return False