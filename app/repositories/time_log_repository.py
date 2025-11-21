from datetime import datetime
from bson import ObjectId

from app.repositories.db import get_db


def start_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    active_timer = time_logs.find_one({
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id),
        'end_time': None
    })

    if active_timer:
        return None

    time_log_doc = {
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id),
        'start_time': datetime.utcnow(),
        'end_time': None,
        'duration_minutes': None
    }

    result = time_logs.insert_one(time_log_doc)
    time_log_doc['_id'] = result.inserted_id
    return time_log_doc


def stop_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    active_timer = time_logs.find_one({
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id),
        'end_time': None
    })

    if not active_timer:
        return None

    end_time = datetime.utcnow()
    duration_minutes = int((end_time - active_timer['start_time']).total_seconds() / 60)

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

    return list(time_logs.find({
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id)
    }).sort('start_time', -1))


def get_active_timer(user_id, project_id):
    db = get_db()
    time_logs = db.time_logs

    return time_logs.find_one({
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id),
        'end_time': None
    })

