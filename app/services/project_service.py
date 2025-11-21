from app.repositories.project_repository import (
    create_project,
    get_projects_for_user,
    get_project_by_id,
    update_project,
    update_project_status,
    delete_project
)


def create_project_for_user(user_id, data):
    return create_project(user_id, data)


def get_user_projects(user_id):
    return get_projects_for_user(user_id)


def get_user_project(user_id, project_id):
    project = get_project_by_id(user_id, project_id)
    if not project:
        return None, 'Project not found'
    return project, None


def update_user_project(user_id, project_id, data):
    project = update_project(user_id, project_id, data)
    if not project:
        return None, 'Project not found'
    return project, None


def change_project_status(user_id, project_id, status):
    project = update_project_status(user_id, project_id, status)
    if not project:
        return None, 'Project not found or invalid status'
    return project, None


def remove_user_project(user_id, project_id):
    deleted = delete_project(user_id, project_id)
    if not deleted:
        return False, 'Project not found'
    return True, None

