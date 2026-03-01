import asyncio
import logging
import os
from aiohttp import web
from redis.asyncio import Redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def on_startup(**kwargs):
    b = kwargs['bot']
    await init_db()
    if not IS_POLLING:
        await b.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    try: await b.send_message(ADMIN_ID, "✅ Бот запущен")
    except: pass

async def on_shutdown(**kwargs):
    b = kwargs['bot']
    await redis_client.close()
    if not IS_POLLING:
        await b.delete_webhook(drop_pending_updates=True)

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
    except (KeyboardInterrupt, SystemExit): pass