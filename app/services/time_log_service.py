from app.repositories.time_log_repository import (
    start_timer,
    stop_timer,
    get_time_logs_for_project,
    get_active_timer
)


def start_timer_for_user(user_id, project_id):
    timer = start_timer(user_id, project_id)
    if not timer:
        return None, 'Timer already running for this project'
    return timer, None


def stop_timer_for_user(user_id, project_id):
    timer = stop_timer(user_id, project_id)
    if not timer:
        return None, 'No active timer found'
    return timer, None


def get_project_time_logs(user_id, project_id):
    return get_time_logs_for_project(user_id, project_id)


def get_user_active_timer(user_id, project_id):
    return get_active_timer(user_id, project_id)

