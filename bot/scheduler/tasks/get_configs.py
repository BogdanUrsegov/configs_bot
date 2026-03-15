import asyncio
import httpx
import re
from datetime import datetime, timezone, timedelta
from aiogram import Bot, types
from aiogram.exceptions import TelegramAPIError

# Импорт вашей функции сохранения в БД
from bot.database.utils.update_config_cache import update_config_cache
from bot.create_bot import bot
from bot.modules.constants import TEXT_UNDER_FILES
from bot.utils.broadcast import broadcast

REPO_RAW = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main"
ORIGINAL_FILES = [
    "WHITE-CIDR-RU-checked.txt",
    "Vless-Reality-White-Lists-Rus-Mobile.txt",
]
NEW_NAMES = [
    "All-checked.txt",
    "For-mobiles.txt",
]
COMMENT_LINE = "# For more info and VPN-configs - visit: www.github.com/igareck/vpn-configs-for-russia"
DATE_PATTERN = re.compile(r"# Date/Time:\s*(\d{4}-\d{2}-\d{2})\s*/\s*(\d{2}:\d{2})")

async def fetch_and_process(client: httpx.AsyncClient, filename: str) -> tuple[bytes, int, str]:
    """
    Скачивает файл, чистит комментарий, парсит дату.
    Возвращает: (контент в байтах, timestamp в секундах, читаемая дата строка).
    """
    url = f"{REPO_RAW}/{filename}"
    resp = await client.get(url, timeout=15.0)
    resp.raise_for_status()
    
    text = resp.text
    lines = text.splitlines()
    
    # 1. Парсинг даты
    timestamp = 0
    date_str_readable = "Неизвестно"
    
    for line in lines[:5]:
        match = DATE_PATTERN.search(line)
        if match:
            date_part, time_part = match.groups()
            dt_str = f"{date_part} {time_part}"
            try:
                # Время в файле московское, конвертируем в UTC для хранения
                dt_naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                dt_utc = dt_naive.replace(tzinfo=timezone.utc) - timedelta(hours=3)
                timestamp = int(dt_utc.timestamp())
                date_str_readable = dt_str # Сохраняем оригинальную строку для красоты
            except ValueError:
                pass
            break

    # 2. Очистка контента
    cleaned_lines = [line for line in lines if line.strip() != COMMENT_LINE]
    cleaned_text = "\n".join(cleaned_lines)
    
    return cleaned_text.encode("utf-8"), timestamp, date_str_readable

async def send_and_save_configs(chat_id: int) -> bool:
    """
    Скачивает конфиги, отправляет их пользователю и сохраняет file_id + время в БД.
    """
    async with httpx.AsyncClient() as client:
        # 1. Параллельная загрузка и обработка
        tasks = [fetch_and_process(client, name) for name in ORIGINAL_FILES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        media_group = []
        data_for_db = {} # Словарь для сбора данных перед записью в БД

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue
            
            content, ts_updated, date_str = result
            
            # Подпись только для второго файла (индекс 1)
            caption = None
            if i == 1:
                readable_date = datetime.fromtimestamp(ts_updated, tz=timezone.utc).strftime("%d.%m.%Y %H:%M") if ts_updated else "Неизвестно"
                caption = TEXT_UNDER_FILES.format(date_str=date_str)
            
            media_group.append(
                types.InputMediaDocument(
                    media=types.BufferedInputFile(file=content, filename=NEW_NAMES[i]),
                    caption=caption,
                    parse_mode="HTML"
                )
            )
            
            # Сохраняем данные для БД (используем тот же timestamp, что и в файле)
            if i == 0:
                data_for_db['full_ts'] = ts_updated
                data_for_db['full_date'] = date_str
            elif i == 1:
                data_for_db['mobile_ts'] = ts_updated
                data_for_db['mobile_date'] = date_str

        if not media_group:
            return False

        try:
            # 2. Отправка файлов
            sent_messages = await bot.send_media_group(chat_id=chat_id, media=media_group)
            
            # 3. Получение file_id из ответа Telegram
            # sent_messages — это список объектов Message. Берем document.file_id
            if len(sent_messages) >= 2:
                full_file_id = sent_messages[0].document.file_id
                mobile_file_id = sent_messages[1].document.file_id
                
                # Используем время из мобильного файла (или полного, они должны совпадать по дате генерации)
                final_ts = data_for_db.get('mobile_ts') or data_for_db.get('full_ts')
                final_date = data_for_db.get('mobile_date') or data_for_db.get('full_date')

                # 4. Запись в БД
                db_success = await update_config_cache(
                    full_file_id=full_file_id,
                    mobile_file_id=mobile_file_id,
                    date_str=final_date,
                    date_ts=final_ts
                )
                
                if db_success:
                    await broadcast()
                
                return True
            else:
                return False

        except TelegramAPIError as e:
            await bot.send_message(chat_id, f"❌ Ошибка отправки: {e}")
            return False