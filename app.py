from flask import render_template, Flask


app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('welcome.html')


#app.run()
