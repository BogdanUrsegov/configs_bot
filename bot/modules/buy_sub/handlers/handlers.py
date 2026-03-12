from aiogram import F, Bot, Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards.inline_keyboards import BUY_SUB_CALL
from bot.modules.constants import PRICE_WEEK
from aiogram.types import LabeledPrice
from bot.database.utils.set_subscription_week import set_subscription_week

router = Router()

@router.callback_query(F.data == BUY_SUB_CALL)
async def buy_sub_call(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.edit_reply_markup()
    user_id = callback.from_user.id
    await bot.send_invoice(
        chat_id=user_id,
        title="Оплата подписки на неделю",
        description="После оплаты у вас появится доступ к файлам с бесплатными конфигурациями Vless",
        payload=f"sub_{user_id}",  # Лучше делать payload уникальным
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Услуга", amount=PRICE_WEEK)],
        start_parameter="stars_payment",
        need_name=False,
        need_email=False,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False,
    )

@router.pre_checkout_query()
async def process_pre_checkout(query: types.PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    user_id = message.from_user.id
    await set_subscription_week(user_id)
    from bot.modules.start.keyboards.inline_keyboards import back_menu
    await message.answer(
        "✅ <b>Оплата прошла успешно!</b>\n\n"
                         
        "📲 <i>Вернитесь обратно и нажмите кнопку для получения свежих конфигураций</i>",
        reply_markup=back_menu
    )