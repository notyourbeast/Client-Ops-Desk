from datetime import datetime
from bson import ObjectId

from app.repositories.db import get_db


def create_client(user_id, data):
    db = get_db()
    clients = db.clients

    client_doc = {
        'user_id': ObjectId(user_id),
        'name': data.get('name', ''),
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'company': data.get('company', ''),
        'notes': data.get('notes', ''),
        'created_at': datetime.utcnow()
    }

    result = clients.insert_one(client_doc)
    client_doc['_id'] = result.inserted_id
    return client_doc


def get_clients_for_user(user_id):
    db = get_db()
    clients = db.clients

    return list(clients.find({'user_id': ObjectId(user_id)}))


def get_client_by_id(user_id, client_id):
    db = get_db()
    clients = db.clients

    return clients.find_one({
        '_id': ObjectId(client_id),
        'user_id': ObjectId(user_id)
    })


def update_client(user_id, client_id, data):
    db = get_db()
    clients = db.clients

    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'email' in data:
        update_fields['email'] = data['email']
    if 'phone' in data:
        update_fields['phone'] = data['phone']
    if 'company' in data:
        update_fields['company'] = data['company']
    if 'notes' in data:
        update_fields['notes'] = data['notes']

    result = clients.update_one(
        {'_id': ObjectId(client_id), 'user_id': ObjectId(user_id)},
        {'$set': update_fields}
    )

    if result.matched_count == 0:
        return None

    return get_client_by_id(user_id, client_id)


def delete_client(user_id, client_id):
    db = get_db()
    clients = db.clients

    result = clients.delete_one({
        '_id': ObjectId(client_id),
        'user_id': ObjectId(user_id)
    })

    return result.deleted_count > 0

