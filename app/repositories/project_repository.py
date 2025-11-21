from datetime import datetime
from bson import ObjectId

from app.repositories.db import get_db


def create_project(user_id, data):
    db = get_db()
    projects = db.projects

    project_doc = {
        'user_id': ObjectId(user_id),
        'client_id': ObjectId(data['client_id']) if data.get('client_id') else None,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'status': data.get('status', 'idea'),
        'hourly_rate': float(data.get('hourly_rate', 0)) if data.get('hourly_rate') else None,
        'deadline': datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
        'created_at': datetime.utcnow()
    }

    result = projects.insert_one(project_doc)
    project_doc['_id'] = result.inserted_id
    return project_doc


def get_projects_for_user(user_id):
    db = get_db()
    projects = db.projects

    return list(projects.find({'user_id': ObjectId(user_id)}))


def get_project_by_id(user_id, project_id):
    db = get_db()
    projects = db.projects

    return projects.find_one({
        '_id': ObjectId(project_id),
        'user_id': ObjectId(user_id)
    })


def update_project(user_id, project_id, data):
    db = get_db()
    projects = db.projects

    update_fields = {}
    if 'title' in data:
        update_fields['title'] = data['title']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'status' in data:
        update_fields['status'] = data['status']
    if 'hourly_rate' in data:
        update_fields['hourly_rate'] = float(data['hourly_rate']) if data['hourly_rate'] else None
    if 'client_id' in data:
        update_fields['client_id'] = ObjectId(data['client_id']) if data['client_id'] else None
    if 'deadline' in data:
        if data['deadline']:
            update_fields['deadline'] = datetime.fromisoformat(data['deadline'])
        else:
            update_fields['deadline'] = None

    result = projects.update_one(
        {'_id': ObjectId(project_id), 'user_id': ObjectId(user_id)},
        {'$set': update_fields}
    )

    if result.matched_count == 0:
        return None

    return get_project_by_id(user_id, project_id)


def update_project_status(user_id, project_id, status):
    db = get_db()
    projects = db.projects

    valid_statuses = ['idea', 'talks', 'in-progress', 'review', 'completed']
    if status not in valid_statuses:
        return None

    result = projects.update_one(
        {'_id': ObjectId(project_id), 'user_id': ObjectId(user_id)},
        {'$set': {'status': status}}
    )

    if result.matched_count == 0:
        return None

    return get_project_by_id(user_id, project_id)


def delete_project(user_id, project_id):
    db = get_db()
    projects = db.projects

    result = projects.delete_one({
        '_id': ObjectId(project_id),
        'user_id': ObjectId(user_id)
    })

    return result.deleted_count > 0

