from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_in.html', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

app.debug = True
app.run()
