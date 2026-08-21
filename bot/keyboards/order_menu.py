from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_order_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Tasdiqlash",
        callback_data="confirm_order"
    )

    builder.button(
        text="❌ Bekor qilish",
        callback_data="cancel_order"
    )

    return builder.as_markup()


def payment_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🧾 Chek yuborish",
        callback_data="send_receipt"
    )

    builder.button(
        text="❌ Bekor qilish",
        callback_data="cancel_order"
    )

    return builder.as_markup()
