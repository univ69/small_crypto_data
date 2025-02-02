from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env

APIKEY_COINGECKO = os.getenv("APIKEY_COINGECKO")

