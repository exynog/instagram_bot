from aiogram import Router, F
from aiogram.types import Message

from database.users import get_user


router = Router()


@router.message(F.text == "🎁 Referral")
async def referral_handler(message: Message):
    user = get_user(
        message.from_user.id
    )

    if not user:
        await message.answer(
            "Profil topilmadi."
        )
        return

    referral_balance = user[4]

    bot_info = await message.bot.get_me()

    link = (
        f"https://t.me/"
        f"{bot_info.username}"
        f"?start={message.from_user.id}"
    )

    await message.answer(
        "🎁 Referral\n\n"
        f"🎁 Bonus buyurtmalar: {referral_balance}\n\n"
        "Har bir yangi tasdiqlangan referral "
        "uchun 1 ta bonus-buyurtma olasiz.\n\n"
        "🔗 Sizning linkingiz:\n"
        f"{link}"
    )