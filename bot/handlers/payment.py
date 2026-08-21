from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.order import OrderState
from database.orders import (
    get_order,
    set_payment_receipt
)

from config import ADMIN_ID


router = Router()


@router.callback_query(
    F.data == "send_receipt"
)
async def send_receipt_button(
    callback,
    state: FSMContext
):
    await callback.message.answer(
        "🧾 To‘lov chekini rasm sifatida yuboring."
    )

    await callback.answer()


@router.message(
    OrderState.waiting_receipt,
    F.photo
)
async def receive_receipt(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    order_id = data.get("order_id")

    if not order_id:
        await message.answer(
            "❌ Buyurtma topilmadi."
        )
        return

    photo = message.photo[-1]

    set_payment_receipt(
        order_id=order_id,
        receipt_file_id=photo.file_id
    )

    order = get_order(order_id)

    if not order:
        await message.answer(
            "❌ Buyurtma topilmadi."
        )
        return

    await message.answer(
        f"🧾 Chek qabul qilindi.\n\n"
        f"🆔 Buyurtma: #{order_id}\n"
        "⏳ Admin to‘lovni tekshirmoqda."
    )

    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=(
            f"🧾 YANGI TO‘LOV\n\n"
            f"🆔 Buyurtma: #{order_id}\n"
            f"👤 Telegram ID: {order[1]}\n"
            f"📸 Instagram: {order[2]}\n"
            f"📊 Miqdor: {order[4]}\n"
            f"💰 Summa: {order[5]:,} so‘m"
        )
    )

    await state.clear()
