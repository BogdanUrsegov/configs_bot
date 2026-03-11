import asyncio
import logging
import os
from aiohttp import web
from redis.asyncio import Redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.middlewares.logging import TelegramLogHandler
from bot.scheduler.tasks.get_configs import send_and_save_configs


from bot.database.session import init_db
from .create_bot import bot, ADMIN_ID
from .routers import router

# Настройки
REDIS_URL = os.getenv("REDIS_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
BASE_URL = os.getenv("WEBHOOK_BASE_URL", "")
HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
PORT = int(os.getenv("WEBHOOK_PORT", "8000"))
IS_POLLING = os.getenv("IS_POLLING", "1").strip().lower() in ("1", "true", "yes", "on")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
# logger.addHandler(TelegramLogHandler(bot=bot, chat_id=LOG_CHANNEL_ID))


scheduler = AsyncIOScheduler()


async def on_startup():
    await init_db()

    logger.info("🔄 Первичная загрузка конфигов перед стартом бота...")
    try:
        await send_and_save_configs(chat_id=ADMIN_ID)
        logger.info("✅ Конфиги успешно загружены и сохранены в БД.")
    except Exception as e:
        logger.error(f"❌ Ошибка первичной загрузки конфигов: {e}")

    scheduler.configure(job_defaults={
        'coalesce': False,
        'max_instances': 1,
        'misfire_grace_time': 60
    })
    
    scheduler.add_job(
        func=send_and_save_configs,
        trigger='interval',
        seconds=3600,
        id=f'send_and_save_configs',
        replace_existing=True,
        misfire_grace_time=None,
        kwargs={'chat_id': ADMIN_ID}
    )

    scheduler.start()
    logger.info("✅ Scheduler started")

    if not IS_POLLING:
        await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    await bot.send_message(ADMIN_ID, "✅ Бот запущен")

async def on_shutdown():
    await bot.send_message(ADMIN_ID, "✋ Бот остановлен")
    await redis_client.close()
    if not IS_POLLING:
        await bot.delete_webhook(drop_pending_updates=True)

def create_dispatcher():
    global redis_client
    redis_client = Redis.from_url(REDIS_URL)
    dp = Dispatcher(storage=RedisStorage(redis=redis_client))
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp

async def run_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    dp = create_dispatcher()
    await dp.start_polling(bot)

def run_webhook():
    dp = create_dispatcher()
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)

if __name__ == "__main__":
    try:
        if IS_POLLING: asyncio.run(run_polling())
        else: run_webhook()
    except (KeyboardInterrupt, SystemExit): 
        pass