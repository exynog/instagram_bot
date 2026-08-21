from aiogram import Router, F
from aiogram.types import Message

from database.users import get_user


router = Router()


@router.message(F.text == "👤 Profil")
async def profile_handler(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer(
            "Profil topilmadi."
        )
        return

    (
        _,
        telegram_id,
        username,
        first_order_used,
        referral_balance,
        referred_by,
        created_at
    ) = user

    username_text = (
        f"@{username}"
        if username
        else "username yo‘q"
    )

    await message.answer(
        "👤 Profil\n\n"
        f"🆔 ID: {telegram_id}\n"
        f"👤 Username: {username_text}\n"
        f"🎁 Bonuslar: {referral_balance}\n"
        f"📅 Ro‘yxatdan o‘tgan: {created_at}"
    )