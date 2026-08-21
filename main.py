import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.init_db import init_db

from config import BOT_TOKEN

from bot.keyboards.main_menu import main_menu

from bot.handlers.profile import router as profile_router
from bot.handlers.referral import router as referral_router
from bot.handlers.order import router as order_router
from bot.handlers.orders_history import (
    router as orders_history_router
)
from bot.handlers.payment import router as payment_router
from bot.handlers.admin import router as admin_router

from database.users import create_user, get_user
from database.referrals import (
    create_referral,
    referral_exists
)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username

    args = message.text.split()

    referral_id = None

    if len(args) > 1:
        try:
            referral_id = int(args[1])
        except ValueError:
            referral_id = None

    existing_user = get_user(
        telegram_id
    )

    if existing_user is None:
        create_user(
            telegram_id=telegram_id,
            username=username,
            referred_by=referral_id
        )

        if (
            referral_id
            and referral_id != telegram_id
            and not referral_exists(telegram_id)
        ):
            referrer = get_user(
                referral_id
            )

            if referrer:
                create_referral(
                    referrer_id=referral_id,
                    referred_id=telegram_id
                )

    await message.answer(
        "Salom! 👋\n\n"
        "Botimizga xush kelibsiz!",
        reply_markup=main_menu()
    )


async def main():
        init_db()
    print("Bot ishga tushdi...")

    dp.include_router(
        profile_router
    )

    dp.include_router(
        referral_router
    )

    dp.include_router(
        order_router
    )

    dp.include_router(
        orders_history_router
    )

    dp.include_router(
        payment_router
    )

    dp.include_router(
        admin_router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())