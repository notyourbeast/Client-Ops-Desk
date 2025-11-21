from datetime import datetime


def create_user_document(email, password_hash, name):
    return {
        'email': email,
        'password_hash': password_hash,
        'name': name,
        'created_at': datetime.utcnow()
    }

