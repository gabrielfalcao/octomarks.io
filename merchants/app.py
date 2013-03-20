from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

assets.load_path.append(assets.get_directory())
assets.register('css', Bundle('style.css'))


@app.route('/')
def index():
    return render_template('index.html')
