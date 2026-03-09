import asyncio
import httpx
from aiogram import Bot, types
from aiogram.exceptions import TelegramAPIError

REPO_RAW = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main"
FILES = {
    "WHITE-CIDR-RU-checked.txt": "🇷🇺 CIDR диапазоны РФ",
    "Vless-Reality-White-Lists-Rus-Mobile.txt": "📱 VLESS Reality WhiteList (Mobile)",
}
COMMENT_LINE = "# For more info and VPN-configs - visit: www.github.com/igareck/vpn-configs-for-russia"

async def fetch_and_process(client: httpx.AsyncClient, filename: str) -> bytes:
    """Скачивает, чистит от комментариев и возвращает байты."""
    url = f"{REPO_RAW}/{filename}"
    resp = await client.get(url, timeout=15.0)
    resp.raise_for_status()
    
    text = resp.text
    cleaned_lines = [line for line in text.splitlines() if line.strip() != COMMENT_LINE]
    return "\n".join(cleaned_lines).encode("utf-8")

async def send_config_files(bot: Bot, chat_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_and_process(client, name) for name in FILES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        media_group = []
        for filename, result in zip(FILES.keys(), results):
            if isinstance(result, Exception):
                continue
            
            media_group.append(
                types.InputMediaDocument(
                    media=types.BufferedInputFile(file=result, filename=filename)
                )
            )

        if not media_group:
            return False

        try:
            await bot.send_media_group(chat_id=chat_id, media=media_group)
            return True
        except TelegramAPIError as e:
            await bot.send_message(chat_id, f"❌ Ошибка отправки: {e}")
            return False