import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "database.db"


def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_order_used INTEGER DEFAULT 0,
            referral_balance INTEGER DEFAULT 0,
            referred_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            instagram_username TEXT NOT NULL,
            service TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER DEFAULT 0,
            status TEXT DEFAULT 'new',
            payment_status TEXT DEFAULT 'pending',
            payment_amount INTEGER DEFAULT 0,
            receipt_file_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER UNIQUE NOT NULL,
            status TEXT DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database tayyor!")


if __name__ == "__main__":
    init_db()