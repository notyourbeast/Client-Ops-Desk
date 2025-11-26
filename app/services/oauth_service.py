from datetime import datetime
from app.repositories.db import get_db


def get_or_create_google_user(google_user_info):
    """
    Get existing user or create new user from Google OAuth data.
    
    Args:
        google_user_info: Dict with 'email', 'name', 'sub' (Google ID)
    
    Returns:
        tuple: (user_doc, error_message)
    """
    db = get_db()
    users = db.users
    
    email = google_user_info.get('email')
    if not email:
        return None, 'Email not provided by Google'
    
    # Check if user exists
    existing_user = users.find_one({'email': email})
    
    if existing_user:
        # User exists, return it
        existing_user.pop('password_hash', None)
        return existing_user, None
    
    # Create new user
    user_doc = {
        'email': email,
        'name': google_user_info.get('name', ''),
        'google_id': google_user_info.get('sub'),
        'auth_provider': 'google',
        'password_hash': None,
        'created_at': datetime.utcnow()
    }
    
    result = users.insert_one(user_doc)
    user_doc['_id'] = result.inserted_id
    user_doc.pop('password_hash', None)
    
    return user_doc, None


def find_user_by_google_id(google_id):
    """
    Find user by Google ID.
    
    Args:
        google_id: Google user ID (sub)
    
    Returns:
        user document or None
    """
    db = get_db()
    users = db.users
    
    user = users.find_one({'google_id': google_id})
    if user:
        user.pop('password_hash', None)
    return user

