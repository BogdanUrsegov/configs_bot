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
        # Устанавливаем минимальный уровень для этого хендлера
        self.setLevel(logging.WARNING)

    def emit(self, record):
        # 1. Фильтр по уровню (дублирующая защита, хотя setLevel уже работает)
        if record.levelno < logging.WARNING:
            return

        msg_str = self.format(record)
        
        # Пропуск служебных сообщений
        if "is handled" in msg_str:
            return

        # Обрезка
        if len(msg_str) > self.max_len:
            msg_str = msg_str[:self.max_len] + "\n... (обрезано)"

        # Эмодзи и экранирование
        prefix = "⚠️ WARNING" if record.levelno == logging.WARNING else "❌ ERROR"
        safe_msg = f"<b>{prefix}</b>\n{html.escape(msg_str)}"

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self.bot.send_message(self.chat_id, safe_msg, parse_mode="HTML")
            )
        except RuntimeError:
            # Цикл еще не запущен (редкий случай для рантайм-ошибок)
            pass 
        except Exception:
            self.handleError(record)