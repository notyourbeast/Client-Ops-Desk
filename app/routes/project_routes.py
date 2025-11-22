from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from bson import ObjectId

from app.services.project_service import create_project_for_user, get_user_projects, change_project_status, get_user_project
from app.services.client_service import get_user_clients
from app.services.time_log_service import start_timer_for_user, stop_timer_for_user, get_user_active_timer
from app.utils.auth_decorators import login_required

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('', methods=['GET'])
@login_required
def list_projects():
    user_id = str(g.current_user['_id'])
    projects = get_user_projects(user_id)
    clients = get_user_clients(user_id)

    client_map = {str(client['_id']): client for client in clients}

    for project in projects:
        if project.get('client_id'):
            project['client_name'] = client_map.get(str(project['client_id']), {}).get('name', 'Unknown')
        else:
            project['client_name'] = None

        active_timer = get_user_active_timer(user_id, str(project['_id']))
        if active_timer:
            project['active_timer'] = {
                'start_time': active_timer['start_time'].isoformat(),
                '_id': str(active_timer['_id'])
            }

    return render_template('projects/list.html', projects=projects, clients=clients)


@projects_bp.route('', methods=['POST'])
@login_required
def create_project():
    user_id = str(g.current_user['_id'])
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'status': request.form.get('status', 'idea'),
        'client_id': request.form.get('client_id', '').strip() or None,
        'hourly_rate': request.form.get('hourly_rate', '').strip() or None,
        'deadline': request.form.get('deadline', '').strip() or None
    }

    if not data['title']:
        flash('Title is required', 'error')
        return redirect(url_for('projects.list_projects'))

    create_project_for_user(user_id, data)
    flash('Project created successfully', 'success')
    return redirect(url_for('projects.list_projects'))


@projects_bp.route('/<project_id>/status', methods=['POST'])
@login_required
def update_status(project_id):
    user_id = str(g.current_user['_id'])
    status = request.json.get('status')

    if not status:
        return jsonify({'error': 'Status is required'}), 400

    project, error = change_project_status(user_id, project_id, status)
    if error:
        return jsonify({'error': error}), 404

    return jsonify({'success': True, 'status': project['status']})


@projects_bp.route('/<project_id>/start-timer', methods=['POST'])
@login_required
def start_timer(project_id):
    user_id = str(g.current_user['_id'])
    timer, error = start_timer_for_user(user_id, project_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'success': True, 'start_time': timer['start_time'].isoformat()})


@projects_bp.route('/<project_id>/stop-timer', methods=['POST'])
@login_required
def stop_timer(project_id):
    user_id = str(g.current_user['_id'])
    timer, error = stop_timer_for_user(user_id, project_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'success': True, 'duration_minutes': timer['duration_minutes']})


@projects_bp.route('/<project_id>/edit', methods=['GET'])
@login_required
def edit_project(project_id):
    user_id = str(g.current_user['_id'])
    project, error = get_user_project(user_id, project_id)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('projects.list_projects'))
    
    clients = get_user_clients(user_id)
    return render_template('projects/edit.html', project=project, clients=clients)

