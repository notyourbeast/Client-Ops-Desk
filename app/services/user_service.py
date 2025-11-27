"""
User Service
Handles user profile management and preferences
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

from app.repositories.db import get_db


def get_user_profile(user_id):
    """
    Get user profile information
    
    Args:
        user_id: User ID (string or ObjectId)
    
    Returns:
        dict: User profile data (without password_hash)
    """
    db = get_db()
    users = db.users
    
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    
    # Remove sensitive data
    user.pop('password_hash', None)
    return user


def update_user_profile(user_id, data):
    """
    Update user profile information
    
    Args:
        user_id: User ID (string or ObjectId)
        data: Dictionary with fields to update (name, email, etc.)
    
    Returns:
        tuple: (updated_user_dict, error_message)
    """
    db = get_db()
    users = db.users
    
    # Check if email is being changed and if it's already taken
    if 'email' in data:
        existing = users.find_one({
            'email': data['email'],
            '_id': {'$ne': ObjectId(user_id)}
        })
        if existing:
            return None, 'Email already in use'
    
    # Build update fields
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'email' in data:
        update_fields['email'] = data['email']
    
    update_fields['updated_at'] = datetime.utcnow()
    
    if not update_fields:
        return None, 'No fields to update'
    
    result = users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update_fields}
    )
    
    if result.modified_count == 0:
        return None, 'Failed to update profile'
    
    # Return updated user
    user = users.find_one({'_id': ObjectId(user_id)})
    user.pop('password_hash', None)
    return user, None


def change_password(user_id, current_password, new_password):
    """
    Change user password
    
    Args:
        user_id: User ID (string or ObjectId)
        current_password: Current password
        new_password: New password
    
    Returns:
        tuple: (success: bool, error_message)
    """
    db = get_db()
    users = db.users
    
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return False, 'User not found'
    
    # Check if user has a password (Google OAuth users might not)
    if 'password_hash' not in user:
        return False, 'Password change not available for OAuth accounts'
    
    # Verify current password
    if not check_password_hash(user['password_hash'], current_password):
        return False, 'Current password is incorrect'
    
    # Update password
    new_password_hash = generate_password_hash(new_password)
    result = users.update_one(
        {'_id': ObjectId(user_id)},
        {
            '$set': {
                'password_hash': new_password_hash,
                'updated_at': datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        return False, 'Failed to update password'
    
    return True, None


def get_user_preferences(user_id):
    """
    Get user preferences
    
    Args:
        user_id: User ID (string or ObjectId)
    
    Returns:
        dict: User preferences
    """
    db = get_db()
    users = db.users
    
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    
    # Return preferences or empty dict
    return user.get('preferences', {})


def update_user_preferences(user_id, preferences):
    """
    Update user preferences
    
    Args:
        user_id: User ID (string or ObjectId)
        preferences: Dictionary of preferences to update
    
    Returns:
        tuple: (updated_preferences, error_message)
    """
    db = get_db()
    users = db.users
    
    # Get current preferences
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None, 'User not found'
    
    current_preferences = user.get('preferences', {})
    
    # Merge with new preferences
    current_preferences.update(preferences)
    
    # Update in database
    result = users.update_one(
        {'_id': ObjectId(user_id)},
        {
            '$set': {
                'preferences': current_preferences,
                'updated_at': datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        return None, 'Failed to update preferences'
    
    return current_preferences, None

