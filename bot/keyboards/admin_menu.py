from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_admin_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ To‘lovni tasdiqlash",
        callback_data=f"approve_payment:{order_id}"
    )

    builder.button(
        text="❌ To‘lovni rad etish",
        callback_data=f"reject_payment:{order_id}"
    )

    return builder.as_markup()


def order_admin_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="▶️ Jarayonga olish",
        callback_data=f"processing:{order_id}"
    )

    builder.button(
        text="✅ Bajarildi",
        callback_data=f"complete:{order_id}"
    )

    builder.button(
        text="❌ Bekor qilish",
        callback_data=f"cancel:{order_id}"
    )

    return builder.as_markup()