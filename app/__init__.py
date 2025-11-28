from datetime import datetime
from flask import Flask, render_template, g, redirect, url_for
from bson import ObjectId

from .config import Config
from .routes.auth_routes import auth_bp
from .routes.client_routes import clients_bp
from .routes.project_routes import projects_bp
from .routes.invoice_routes import invoices_bp
from .routes.time_routes import time_bp
from .routes.search_routes import search_bp
from .services.client_service import get_user_clients
from .services.project_service import get_user_projects
from .services.invoice_service import get_user_invoices
from .repositories.time_log_repository import get_time_logs_for_project
from .repositories.db import get_db
from .utils.auth_decorators import login_required


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Handle proxy headers for HTTPS detection (Render, etc.)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize OAuth
    from authlib.integrations.flask_client import OAuth
    oauth = OAuth(app)
    
    if Config.GOOGLE_CLIENT_ID and Config.GOOGLE_CLIENT_SECRET:
        # Configure Flask URL generation for OAuth redirects
        if Config.SERVER_NAME:
            app.config['SERVER_NAME'] = Config.SERVER_NAME
        if Config.PREFERRED_URL_SCHEME:
            app.config['PREFERRED_URL_SCHEME'] = Config.PREFERRED_URL_SCHEME
        
        google = oauth.register(
            name='google',
            client_id=Config.GOOGLE_CLIENT_ID,
            client_secret=Config.GOOGLE_CLIENT_SECRET,
            server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
            client_kwargs={
                'scope': 'openid email profile'
            },
            # Explicitly set the API base URL to avoid relative URL issues
            api_base_url='https://www.googleapis.com/'
        )
        app.config['GOOGLE_OAUTH'] = google
    else:
        app.config['GOOGLE_OAUTH'] = None

    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(time_bp)
    app.register_blueprint(search_bp)

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

        # Use ObjectId for user_id to ensure proper query
        user_obj_id = g.current_user['_id'] if isinstance(g.current_user['_id'], ObjectId) else ObjectId(g.current_user['_id'])

        monthly_logs = list(time_logs.find({
            'user_id': user_obj_id,
            'end_time': {'$gte': first_day_of_month, '$lte': now},
            'duration_minutes': {'$ne': None}
        }))

        total_hours_this_month = round(sum(log.get('duration_minutes', 0) for log in monthly_logs) / 60, 1)

        weekly_hours = [0.0] * 5
        for log in monthly_logs:
            if log.get('end_time'):
                week_num = (log['end_time'].day - 1) // 7
                if week_num < 5:
                    weekly_hours[week_num] += log.get('duration_minutes', 0) / 60.0
        
        max_hours = max(weekly_hours) if weekly_hours else 1.0
        weekly_hours = [round(h, 1) for h in weekly_hours]

        invoices = get_user_invoices(user_id)
        unpaid_invoices = [inv for inv in invoices if inv.get('status') == 'unpaid']
        unpaid_count = len(unpaid_invoices)
        total_pending = round(sum(inv.get('amount_due', 0) for inv in unpaid_invoices), 2)
        
        paid_invoices_this_month = [inv for inv in invoices 
                                     if inv.get('status') == 'paid' 
                                     and inv.get('created_at') 
                                     and inv['created_at'] >= first_day_of_month]
        monthly_revenue = round(sum(inv.get('amount_due', 0) for inv in paid_invoices_this_month), 2)
        
        project_hours = {}
        project_map = {str(p['_id']): p for p in projects}
        for log in monthly_logs:
            if log.get('project_id') and log.get('duration_minutes'):
                project_id_str = str(log['project_id'])
                if project_id_str not in project_hours:
                    project_hours[project_id_str] = 0
                project_hours[project_id_str] += log.get('duration_minutes', 0) / 60.0
        
        top_projects = []
        for project_id_str, hours in sorted(project_hours.items(), key=lambda x: x[1], reverse=True)[:3]:
            project = project_map.get(project_id_str)
            if project:
                top_projects.append({
                    'title': project.get('title', 'Unknown'),
                    'hours': round(hours, 1)
                })

        metrics = {
            'total_clients': total_clients,
            'active_projects': active_projects,
            'total_hours_this_month': total_hours_this_month,
            'unpaid_invoices_count': unpaid_count,
            'total_pending_amount': total_pending,
            'weekly_hours': weekly_hours,
            'max_hours': max_hours,
            'monthly_revenue': monthly_revenue,
            'top_projects': top_projects
        }

        return render_template('dashboard.html', metrics=metrics)

    return app
