from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.repositories.db import get_db


def register_user(data):
    db = get_db()
    users = db.users

    existing = users.find_one({'email': data['email']})
    if existing:
        return None, 'Email already registered'

    password_hash = generate_password_hash(data['password'])
    user_doc = {
        'email': data['email'],
        'password_hash': password_hash,
        'name': data.get('name', ''),
        'created_at': datetime.utcnow()
    }

    result = users.insert_one(user_doc)
    user_doc['_id'] = result.inserted_id
    user_doc.pop('password_hash', None)

    return user_doc, None


def authenticate_user(email, password):
    db = get_db()
    users = db.users

    user = users.find_one({'email': email})
    if not user:
        return None, 'Invalid credentials'

    if not check_password_hash(user['password_hash'], password):
        return None, 'Invalid credentials'

    user.pop('password_hash', None)
    return user, None

