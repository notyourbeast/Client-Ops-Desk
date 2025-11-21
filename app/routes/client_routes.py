from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from app.services.client_service import create_client_for_user, get_user_clients
from app.utils.auth_decorators import login_required

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')


@clients_bp.route('', methods=['GET'])
@login_required
def list_clients():
    user_id = str(g.current_user['_id'])
    clients = get_user_clients(user_id)
    return render_template('clients/list.html', clients=clients)


@clients_bp.route('', methods=['POST'])
@login_required
def create_client():
    user_id = str(g.current_user['_id'])
    data = {
        'name': request.form.get('name', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'company': request.form.get('company', '').strip(),
        'notes': request.form.get('notes', '').strip()
    }

    if not data['name']:
        flash('Name is required', 'error')
        return redirect(url_for('clients.list_clients'))

    create_client_for_user(user_id, data)
    flash('Client created successfully', 'success')
    return redirect(url_for('clients.list_clients'))

