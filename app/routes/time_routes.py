from flask import Blueprint, render_template, g

from app.services.time_log_service import get_all_user_time_logs
from app.services.project_service import get_user_projects
from app.utils.auth_decorators import login_required

time_bp = Blueprint('time', __name__, url_prefix='/time')


@time_bp.route('', methods=['GET'])
@login_required
def list_time_logs():
    user_id = str(g.current_user['_id'])
    time_logs = get_all_user_time_logs(user_id)
    projects = get_user_projects(user_id)

    project_map = {str(project['_id']): project for project in projects}

    for log in time_logs:
        if log.get('project_id'):
            project = project_map.get(str(log['project_id']), {})
            log['project_name'] = project.get('title', 'Unknown Project')
        else:
            log['project_name'] = None

    return render_template('time/list.html', time_logs=time_logs)

