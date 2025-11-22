from datetime import datetime
from flask import Flask, render_template, g, redirect, url_for

from .config import Config
from .routes.auth_routes import auth_bp
from .routes.client_routes import clients_bp
from .routes.project_routes import projects_bp
from .routes.invoice_routes import invoices_bp
from .routes.time_routes import time_bp
from .services.client_service import get_user_clients
from .services.project_service import get_user_projects
from .services.invoice_service import get_user_invoices
from .repositories.time_log_repository import get_time_logs_for_project
from .repositories.db import get_db
from .utils.auth_decorators import login_required


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(time_bp)

    @app.route('/')
    def index():
        return render_template('intro.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user_id = str(g.current_user['_id'])

        clients = get_user_clients(user_id)
        total_clients = len(clients)

        projects = get_user_projects(user_id)
        active_projects = len([p for p in projects if p.get('status') != 'completed'])

        now = datetime.utcnow()
        first_day_of_month = datetime(now.year, now.month, 1)
        db = get_db()
        time_logs = db.time_logs

        monthly_logs = list(time_logs.find({
            'user_id': g.current_user['_id'],
            'end_time': {'$gte': first_day_of_month, '$lte': now},
            'duration_minutes': {'$ne': None}
        }))

        total_hours_this_month = round(sum(log.get('duration_minutes', 0) for log in monthly_logs) / 60, 1)

        invoices = get_user_invoices(user_id)
        unpaid_invoices = [inv for inv in invoices if inv.get('status') == 'unpaid']
        unpaid_count = len(unpaid_invoices)
        total_pending = round(sum(inv.get('amount_due', 0) for inv in unpaid_invoices), 2)

        metrics = {
            'total_clients': total_clients,
            'active_projects': active_projects,
            'total_hours_this_month': total_hours_this_month,
            'unpaid_invoices_count': unpaid_count,
            'total_pending_amount': total_pending
        }

        return render_template('dashboard.html', metrics=metrics)

    return app
