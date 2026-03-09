from aiogram import Router
from bot.modules.start import router as start_router
from bot.modules.get_access import router as get_access_router
from bot.modules.extradition import router as extradition_router
from bot.modules.buy_sub import router as buy_sub_router
from bot.modules.profile import router as profile_router
from bot.modules.instruction import router as instruction_router


router = Router()
router.include_routers(
                        start_router, 
                        get_access_router, 
                        extradition_router,
                        buy_sub_router,
                        profile_router,
                        instruction_router
                       )


__all__ = ["router"]