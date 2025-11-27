from datetime import datetime
from bson import ObjectId

from app.repositories.db import get_db


def _to_object_id(value):
    """Convert value to ObjectId, handling both string and ObjectId inputs"""
    if isinstance(value, ObjectId):
        return value
    try:
        return ObjectId(value)
    except (TypeError, ValueError):
        return None


def start_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    user_obj_id = _to_object_id(user_id)
    project_obj_id = _to_object_id(project_id)
    
    if not user_obj_id or not project_obj_id:
        return None

    active_timer = time_logs.find_one({
        'user_id': user_obj_id,
        'project_id': project_obj_id,
        'end_time': None
    })

    if active_timer:
        return None

    time_log_doc = {
        'user_id': user_obj_id,
        'project_id': project_obj_id,
        'start_time': datetime.utcnow(),
        'end_time': None,
        'duration_minutes': None,
        'created_at': datetime.utcnow()
    }

    result = time_logs.insert_one(time_log_doc)
    time_log_doc['_id'] = result.inserted_id
    return time_log_doc


def stop_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    user_obj_id = _to_object_id(user_id)
    project_obj_id = _to_object_id(project_id)
    
    if not user_obj_id or not project_obj_id:
        return None

    active_timer = time_logs.find_one({
        'user_id': user_obj_id,
        'project_id': project_obj_id,
        'end_time': None
    })

    if not active_timer:
        return None

    end_time = datetime.utcnow()
    start_time = active_timer.get('start_time')
    if not start_time:
        return None
    
    duration_minutes = int((end_time - start_time).total_seconds() / 60)

    result = time_logs.update_one(
        {'_id': active_timer['_id']},
        {'$set': {
            'end_time': end_time,
            'duration_minutes': duration_minutes
        }}
    )

    if result.modified_count == 0:
        return None

    active_timer['end_time'] = end_time
    active_timer['duration_minutes'] = duration_minutes
    return active_timer


def get_time_logs_for_project(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    user_obj_id = _to_object_id(user_id)
    project_obj_id = _to_object_id(project_id)
    
    if not user_obj_id or not project_obj_id:
        return []

    return list(time_logs.find({
        'user_id': user_obj_id,
        'project_id': project_obj_id
    }).sort('start_time', -1))


def get_active_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    user_obj_id = _to_object_id(user_id)
    project_obj_id = _to_object_id(project_id)
    
    if not user_obj_id or not project_obj_id:
        return None

    return time_logs.find_one({
        'user_id': user_obj_id,
        'project_id': project_obj_id,
        'end_time': None
    })


def get_all_time_logs_for_user(user_id):
    db = get_db()
    time_logs = db.time_logs

    user_obj_id = _to_object_id(user_id)
    if not user_obj_id:
        return []

    return list(time_logs.find({
        'user_id': user_obj_id
    }).sort('start_time', -1))

