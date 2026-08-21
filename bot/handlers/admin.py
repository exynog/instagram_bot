from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from config import ADMIN_ID

from database.orders import (
    get_order,
    approve_payment,
    reject_payment,
    complete_order,
    cancel_order
)

from bot.keyboards.admin_menu import (
    payment_admin_keyboard,
    order_admin_keyboard
)


router = Router()


def is_admin(user_id: int):
    return user_id == ADMIN_ID


@router.callback_query(
    F.data.startswith("approve_payment:")
)
async def approve_payment_handler(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "Ruxsat yo‘q.",
            show_alert=True
        )
        return

    order_id = int(
        callback.data.split(":")[1]
    )

    order = get_order(order_id)

    if not order:
        await callback.answer(
            "Buyurtma topilmadi.",
            show_alert=True
        )
        return

    approve_payment(order_id)

    await callback.message.edit_caption(
        caption=(
            f"✅ TO‘LOV TASDIQLANDI\n\n"
            f"🆔 Buyurtma: #{order_id}\n"
            f"📸 Instagram: {order[2]}\n"
            f"📊 Miqdor: {order[4]}\n"
            f"💰 {order[5]:,} so‘m"
        ),
        reply_markup=order_admin_keyboard(order_id)
    )

    await callback.bot.send_message(
        chat_id=order[1],
        text=(
            f"✅ To‘lov qabul qilindi!\n\n"
            f"🆔 Buyurtma: #{order_id}\n"
            "⏳ Buyurtma bajarilmoqda..."
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("reject_payment:")
)
async def reject_payment_handler(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "Ruxsat yo‘q.",
            show_alert=True
        )
        return

    order_id = int(
        callback.data.split(":")[1]
    )

    order = get_order(order_id)

    if not order:
        await callback.answer(
            "Buyurtma topilmadi.",
            show_alert=True
        )
        return

    reject_payment(order_id)

    await callback.message.edit_caption(
        caption=(
            f"❌ TO‘LOV RAD ETILDI\n\n"
            f"🆔 Buyurtma: #{order_id}"
        )
    )

    await callback.bot.send_message(
        chat_id=order[1],
        text=(
            f"❌ To‘lov tasdiqlanmadi.\n\n"
            f"🆔 Buyurtma: #{order_id}\n"
            "Iltimos, chekni qayta yuboring."
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("processing:")
)
async def processing_handler(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    order_id = int(
        callback.data.split(":")[1]
    )

    order = get_order(order_id)

    if not order:
        return

    await callback.bot.send_message(
        chat_id=order[1],
        text=(
            f"⏳ Buyurtma #{order_id} "
            "bajarilmoqda."
        )
    )

    await callback.answer(
        "Foydalanuvchiga xabar yuborildi."
    )


@router.callback_query(
    F.data.startswith("complete:")
)
async def complete_handler(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    order_id = int(
        callback.data.split(":")[1]
    )

    order = get_order(order_id)

    if not order:
        return

    complete_order(order_id)

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.bot.send_message(
        chat_id=order[1],
        text=(
            f"✅ Buyurtma #{order_id} "
            "muvaffaqiyatli bajarildi!"
        )
    )

    await callback.answer(
        "Buyurtma bajarildi."
    )


@router.callback_query(
    F.data.startswith("cancel:")
)
async def cancel_handler(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    order_id = int(
        callback.data.split(":")[1]
    )

    order = get_order(order_id)

    if not order:
        return

    cancel_order(order_id)

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.bot.send_message(
        chat_id=order[1],
        text=(
            f"❌ Buyurtma #{order_id} "
            "bekor qilindi."
        )
    )

    await callback.answer(
        "Buyurtma bekor qilindi."
    )