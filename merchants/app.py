from flask import Flask, render_template

from merchants.bundles import create_bundles

app = Flask(__name__)

# Loading our JS/CSS
create_bundles(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard/main.html')


@app.route('/dashboard/competitors/')
def dashboard_competitors():
    return render_template('dashboard/competitors.html')
