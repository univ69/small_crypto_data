import sqlite3


def get_btc_price():
    try:
        with sqlite3.connect('modules/my_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM history_btc_price ORDER BY timestamp DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None


def get_btc_price_change():
    try:
        with sqlite3.connect('modules/my_database.db') as conn:
            cursor = conn.cursor()

            # Получаем последние две цены
            cursor.execute("SELECT price FROM history_btc_price ORDER BY timestamp DESC LIMIT 2")
            results = cursor.fetchall()

            # Проверяем, есть ли хотя бы 2 записи
            if len(results) < 2:
                return None  # Недостаточно данных для расчёта

            latest_price = results[0][0]  # Последняя цена
            previous_price = results[1][0]  # Предыдущая цена

            # Вычисляем изменение в процентах
            price_change = ((latest_price - previous_price) / previous_price) * 100

            return round(price_change, 2)  # Округляем до 2 знаков после запятой

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None