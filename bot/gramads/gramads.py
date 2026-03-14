import logging
import os
import aiohttp

logger = logging.getLogger(__name__)

# Константы вынесены для переиспользования и чистоты кода
GRAMADS_URL = 'https://api.gramads.net/ad/SendPost'
GRAMADS_TOKEN = os.getenv("GRAMADS_TOKEN")

async def show_advert(user_id: int) -> bool:
    """Отправляет рекламу пользователю через GramAds.
    
    Returns:
        bool: True если реклама отправлена успешно, иначе False.
    """
    headers = {
        'Authorization': GRAMADS_TOKEN,
        'Content-Type': 'application/json',
    }
    payload = {'SendToChatId': user_id}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAMADS_URL, headers=headers, json=payload) as response:
                if response.ok:
                    logger.debug(response)
                    return True
                
                error_data = await response.json()
                logger.error('Gramads error: %s', error_data)
                return False

    except Exception as e:
        logger.exception('Gramads request failed: %s', e)
        return False