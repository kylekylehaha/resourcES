from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return 'Hello' + request.values.get('user_id')

    return render_template('sign_up.html')

@app.route('/sign_in.html', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        return 'Hello' + request.values.get('user_id')

    return render_template('sign_in.html')

app.debug = True
app.run()
