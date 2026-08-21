import sqlite3

from database.init_db import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_order(
    telegram_id: int,
    instagram_username: str,
    service: str,
    quantity: int,
    price: int
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO orders (
            telegram_id,
            instagram_username,
            service,
            quantity,
            price,
            status,
            payment_status,
            payment_amount
        )
        VALUES (?, ?, ?, ?, ?, 'new', 'pending', ?)
        """,
        (
            telegram_id,
            instagram_username,
            service,
            quantity,
            price,
            price
        )
    )

    order_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return order_id


def get_order(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            telegram_id,
            instagram_username,
            service,
            quantity,
            price,
            status,
            payment_status,
            payment_amount,
            receipt_file_id,
            created_at
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    connection.close()

    return order


def get_user_orders(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            instagram_username,
            service,
            quantity,
            price,
            status,
            payment_status,
            created_at
        FROM orders
        WHERE telegram_id = ?
        ORDER BY id DESC
        """,
        (telegram_id,)
    )

    orders = cursor.fetchall()

    connection.close()

    return orders


def set_payment_receipt(order_id: int, receipt_file_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET
            receipt_file_id = ?,
            payment_status = 'review',
            status = 'payment_review'
        WHERE id = ?
        """,
        (
            receipt_file_id,
            order_id
        )
    )

    connection.commit()
    connection.close()


def approve_payment(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET
            payment_status = 'approved',
            status = 'processing'
        WHERE id = ?
        """,
        (order_id,)
    )

    connection.commit()
    connection.close()


def reject_payment(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET
            payment_status = 'rejected',
            status = 'payment_waiting'
        WHERE id = ?
        """,
        (order_id,)
    )

    connection.commit()
    connection.close()


def complete_order(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = 'completed'
        WHERE id = ?
        """,
        (order_id,)
    )

    connection.commit()
    connection.close()


def cancel_order(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = 'cancelled'
        WHERE id = ?
        """,
        (order_id,)
    )

    connection.commit()
    connection.close()


def get_orders_by_status(status: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            telegram_id,
            instagram_username,
            service,
            quantity,
            price,
            status,
            payment_status,
            receipt_file_id,
            created_at
        FROM orders
        WHERE status = ?
        ORDER BY id DESC
        """,
        (status,)
    )

    orders = cursor.fetchall()

    connection.close()

    return orders