from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone, date
from typing import Dict, Any

from bot.database.models import User
from bot.database.session import AsyncSessionLocal

async def get_users_stats() -> Dict[str, Any]:
    async with AsyncSessionLocal() as session:

        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)

        # 1. Общее количество
        total_count = (await session.execute(select(func.count(User.id)))).scalar() or 0

        # 2. Активные подписки
        active_subs = (await session.execute(
            select(func.count(User.id)).where(User.subscription_date.isnot(None))
        )).scalar() or 0

        # 3. Статистика по дням
        stats_map: Dict[date, int] = {}

        # Инициализируем все 7 дней нулями (ключи - объекты date)
        for i in range(7):
            d = (now - timedelta(days=i)).date()
            stats_map[d] = 0
            
        # Запрос
        query = select(
            func.date(User.created_at).label('reg_date'),
            func.count(User.id).label('count')
        ).where(
            User.created_at >= week_ago
        ).group_by('reg_date')

        result = await session.execute(query)

        for row in result:
            # Приводим результат func.date() к объекту date, если это строка
            row_date = row.reg_date
            if isinstance(row_date, str):
                row_date = datetime.strptime(row_date, "%Y-%m-%d").date()
            
            if row_date in stats_map:
                stats_map[row_date] = row.count
                
        # Сортировка теперь безопасна, так как все ключи - объекты date
        weekly_growth = [
            {"date": d.isoformat(), "count": c} 
            for d, c in sorted(stats_map.items())
        ]

        return {
            "total": total_count,
            "active_subscriptions": active_subs,
            "weekly_growth": weekly_growth
        }