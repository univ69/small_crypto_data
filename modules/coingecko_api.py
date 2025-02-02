from pycoingecko import CoinGeckoAPI
import sqlite3
from datetime import datetime, timezone, timedelta
import logging
import config

# Настройка логирования в файл
logging.basicConfig(
    filename='coingecko_api.log',  # Файл для логов
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'  # Используем UTF-8 для поддержки русского текста
)
logger = logging.getLogger(__name__)

# Создаём экземпляр API CoinGecko
cg = CoinGeckoAPI(demo_api_key=config.APIKEY_COINGECKO)

class GetFullPrice:
    def __init__(self, ids="bitcoin", vs_currencies="usd"):
        """Инициализация класса с параметрами валюты."""
        self.ids = ids
        self.vs_currencies = vs_currencies

    def get_data_from_api(self):
        """Получаем данные с CoinGecko API."""
        try:
            data = cg.get_price(ids=self.ids, vs_currencies=self.vs_currencies)
            logger.info(f"Успешно получены данные: {data}")
            return data
        except Exception as e:
            logger.error(f"Ошибка при получении данных: {e}")
            return None

    def save_data_from_get_api(self):
        """Сохраняем данные, полученные с API, в базу данных."""
        result_get_api = self.get_data_from_api()
        if result_get_api:
            try:
                with sqlite3.connect('my_database.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS history_btc_price (
                            id TEXT,
                            price REAL,
                            timestamp TEXT)''')

                    coin_name = list(result_get_api.keys())[0]  # Имя криптовалюты
                    coin_price = result_get_api[coin_name]['usd']  # Цена в USD

                    # Получаем текущее время в Киеве (UTC+2 или UTC+3 в зависимости от времени года)
                    kiev_time = datetime.now(timezone(timedelta(hours=2)))  # Киевская зона UTC+2
                    timestamp = kiev_time.strftime('%Y-%m-%d %H:%M:%S')

                    # Вставка данных в таблицу
                    cursor.execute('''
                        INSERT INTO history_btc_price (id, price, timestamp)
                        VALUES (?, ?, ?)
                    ''', (coin_name, coin_price, timestamp))

                    connection.commit()
                    logger.info(f"Данные о цене {coin_name} ({coin_price} USD) сохранены в базу данных.")
            except sqlite3.Error as e:
                logger.error(f"Ошибка при работе с базой данных: {e}")
        else:
            logger.warning("Нет данных для сохранения.")


if __name__ == '__main__':
    get_price = GetFullPrice(ids="bitcoin", vs_currencies="usd")
    get_price.save_data_from_get_api()
