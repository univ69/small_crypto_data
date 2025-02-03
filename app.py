from flask import render_template, Flask
from modules import database_func

app = Flask(__name__)


@app.route('/')
def home_page():
    result = database_func.get_btc_price()
    change_result = database_func.get_btc_price_change()
    btc_price = result
    # Возвращаем HTML-шаблон с результатом
    return render_template('welcome.html', btc_price=btc_price, change_result=change_result)

