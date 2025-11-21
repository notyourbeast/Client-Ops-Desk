from flask import Flask, render_template

from .config import Config


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    @app.route('/')
    def index():
        return 'Freelance ClientHub API'

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    return app
