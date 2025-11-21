from flask import Flask, render_template

from .config import Config
from .routes.auth_routes import auth_bp
from .utils.auth_decorators import login_required


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return 'Freelance ClientHub API'

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    return app
