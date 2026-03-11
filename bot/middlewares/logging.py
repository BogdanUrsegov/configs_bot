import logging
import asyncio
import html
from aiogram import Bot

class TelegramLogHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.max_len = 4000

    def emit(self, record):
        # Фильтр: пропускаем записи, содержащие "is handled"
        msg_str = self.format(record)
        if "is handled" in msg_str:
            return

        # Обрезка до 4000 символов (Telegram limit ~4096, берем с запасом)
        if len(msg_str) > self.max_len:
            msg_str = msg_str[:self.max_len] + "\n... (обрезано)"

        safe_msg = html.escape(msg_str)

        try:
            # Безопасный запуск асинхронной задачи
            asyncio.create_task(
                self.bot.send_message(
                    self.chat_id, 
                    safe_msg
                )
            )
        except Exception:
            self.handleError(record)