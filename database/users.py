import sqlite3

from database.init_db import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_user(
    telegram_id: int,
    username: str | None,
    referred_by: int | None = None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (
            telegram_id,
            username,
            referred_by
        )
        VALUES (?, ?, ?)
        """,
        (
            telegram_id,
            username,
            referred_by
        )
    )

    connection.commit()
    connection.close()


def get_user(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            telegram_id,
            username,
            first_order_used,
            referral_balance,
            referred_by,
            created_at
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def mark_first_order_used(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET first_order_used = 1
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    connection.commit()
    connection.close()


def use_referral_bonus(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET referral_balance = referral_balance - 1
        WHERE telegram_id = ?
        AND referral_balance > 0
        """,
        (telegram_id,)
    )

    changed = cursor.rowcount

    connection.commit()
    connection.close()

    return changed == 1