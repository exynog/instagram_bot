import sqlite3

from database.init_db import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def referral_exists(referred_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM referrals
        WHERE referred_id = ?
        """,
        (referred_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def create_referral(referrer_id: int, referred_id: int):
    if referrer_id == referred_id:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO referrals (
            referrer_id,
            referred_id,
            status
        )
        VALUES (?, ?, 'confirmed')
        """,
        (
            referrer_id,
            referred_id
        )
    )

    if cursor.rowcount == 1:
        cursor.execute(
            """
            UPDATE users
            SET referral_balance = referral_balance + 1
            WHERE telegram_id = ?
            """,
            (referrer_id,)
        )

        connection.commit()
        connection.close()

        return True

    connection.close()

    return False