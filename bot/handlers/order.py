from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.states.order import OrderState
from bot.keyboards.order_menu import (
    confirm_order_keyboard,
    payment_keyboard
)

from database.orders import create_order
from database.users import get_user, use_referral_bonus
from services.services import calculate_price


router = Router()


@router.message(F.text == "🛒 Buyurtma berish")
async def order_start(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer(
            "Avval /start bosing."
        )
        return

    await state.set_state(
        OrderState.waiting_username
    )

    await message.answer(
        "📸 Instagram username va parolini yuboring.\n\n"
        "Masalan:\n"
        "@example_user"
    )


@router.message(OrderState.waiting_username)
async def order_username(
    message: Message,
    state: FSMContext
):
    username = message.text.strip()

    if len(username) < 2:
        await message.answer(
            "❌ Username noto‘g‘ri.\n"
            "Qaytadan yuboring."
        )
        return

    await state.update_data(
        instagram_username=username
    )

    await state.set_state(
        OrderState.waiting_quantity
    )

    await message.answer(
        "📊 Miqdorni kiriting:"
    )


@router.message(OrderState.waiting_quantity)
async def order_quantity(
    message: Message,
    state: FSMContext
):
    try:
        quantity = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ Faqat raqam kiriting."
        )
        return

    if quantity <= 0:
        await message.answer(
            "❌ Miqdor 0 dan katta bo‘lishi kerak."
        )
        return

    price = calculate_price(
        "nakrutka",
        quantity
    )

    if price is None:
        await message.answer(
            "❌ Xizmat topilmadi."
        )
        return

    data = await state.get_data()

    await state.update_data(
        quantity=quantity,
        price=price,
        service="Instagram xizmat"
    )

    await state.set_state(
        OrderState.confirming
    )

    await message.answer(
        "📦 Buyurtma:\n\n"
        f"📸 Instagram: {data['instagram_username']}\n"
        f"📊 Miqdor: {quantity}\n"
        f"💰 Narx: {price:,} so‘m\n\n"
        "Tasdiqlaysizmi?",
        reply_markup=confirm_order_keyboard()
    )


@router.callback_query(F.data == "cancel_order")
async def cancel_order_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "❌ Buyurtma bekor qilindi."
    )

    await callback.answer()


@router.callback_query(
    F.data == "confirm_order"
)
async def confirm_order_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()

    user = get_user(callback.from_user.id)

    if not user:
        await callback.answer(
            "Foydalanuvchi topilmadi.",
            show_alert=True
        )
        return

    first_order_used = user[3]
    referral_balance = user[4]

    is_bonus = False

    if first_order_used == 0:
        pass

    elif referral_balance > 0:
        is_bonus = True

    else:
        pass

    order_id = create_order(
        telegram_id=callback.from_user.id,
        instagram_username=data["instagram_username"],
        service=data["service"],
        quantity=data["quantity"],
        price=0 if is_bonus else data["price"]
    )

    if is_bonus:
        use_referral_bonus(
            callback.from_user.id
        )

    await state.update_data(
        order_id=order_id,
        is_bonus=is_bonus
    )

    await state.set_state(
        OrderState.waiting_receipt
    )

    if is_bonus:
        await callback.message.edit_text(
            f"🎁 Bonus buyurtma #{order_id}\n\n"
            "Buyurtma bonus orqali qabul qilindi."
        )

        await callback.message.answer(
            "⏳ Buyurtma ko‘rib chiqilmoqda."
        )

    else:
        from config import CARD_NUMBER, CARD_OWNER

        await callback.message.edit_text(
            f"📦 Buyurtma #{order_id}\n\n"
            f"💰 To‘lov: {data['price']:,} so‘m\n\n"
            f"💳 Karta: {CARD_NUMBER}\n"
            f"👤 Karta egasi: {CARD_OWNER}\n\n"
            "To‘lovni amalga oshiring va "
            "chekni yuboring."
        )

        await callback.message.answer(
            "🧾 To‘lov chekini rasm sifatida yuboring.",
            reply_markup=payment_keyboard()
        )

    await callback.answer()