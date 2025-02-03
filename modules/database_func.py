import sqlite3


def get_btc_price():
    try:
        with sqlite3.connect('modules/my_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price, timestamp FROM history_btc_price ORDER BY timestamp DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0], result[1] if result else (None, None)
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None, None