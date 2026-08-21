import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

CARD_NUMBER = os.getenv("CARD_NUMBER")
CARD_OWNER = os.getenv("CARD_OWNER")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi!")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID .env faylida topilmadi!")

if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID .env faylida topilmadi!")

if not CARD_NUMBER:
    raise ValueError("CARD_NUMBER .env faylida topilmadi!")