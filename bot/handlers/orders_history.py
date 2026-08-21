from aiogram import Router, F
from aiogram.types import Message

from database.orders import get_user_orders


router = Router()


@router.message(F.text == "📦 Buyurtmalarim")
async def orders_history_handler(
    message: Message
):
    orders = get_user_orders(
        message.from_user.id
    )

    if not orders:
        await message.answer(
            "📦 Hali buyurtmalaringiz yo‘q."
        )
        return

    text = "📦 Buyurtmalarim:\n\n"

    for order in orders:
        (
            order_id,
            instagram,
            service,
            quantity,
            price,
            status,
            payment_status,
            created_at
        ) = order

        text += (
            f"🆔 #{order_id}\n"
            f"📸 {instagram}\n"
            f"📊 {quantity}\n"
            f"💰 {price:,} so‘m\n"
            f"📌 {status}\n"
            f"💳 {payment_status}\n"
            f"📅 {created_at}\n\n"
        )

    await message.answer(text)