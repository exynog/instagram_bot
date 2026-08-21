from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text="🛒 Buyurtma berish")
    builder.button(text="📦 Buyurtmalarim")
    builder.button(text="🎁 Referral")
    builder.button(text="👤 Profil")

    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)