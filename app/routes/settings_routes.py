"""
Settings Routes
Handles user profile and preferences management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify, session
from bson import ObjectId

from app.services.user_service import (
    get_user_profile,
    update_user_profile,
    change_password,
    get_user_preferences,
    update_user_preferences
)
from app.utils.auth_decorators import login_required

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Display user profile settings page"""
    user_id = str(g.current_user['_id'])
    user = get_user_profile(user_id)
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if user has password (not OAuth-only)
    has_password = 'password_hash' in g.current_user
    
    return render_template('settings/profile.html', user=user, has_password=has_password)


@settings_bp.route('/profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    user_id = str(g.current_user['_id'])
    
    data = {
        'name': request.form.get('name', '').strip(),
        'email': request.form.get('email', '').strip()
    }
    
    # Validate
    if not data['name']:
        flash('Name is required', 'error')
        return redirect(url_for('settings.profile'))
    
    if not data['email']:
        flash('Email is required', 'error')
        return redirect(url_for('settings.profile'))
    
    # Update profile
    user, error = update_user_profile(user_id, data)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('settings.profile'))
    
    # Update session if email or name changed
    if session.get('user'):
        session['user']['name'] = user.get('name', '')
        session['user']['email'] = user.get('email', '')
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('settings.profile'))


@settings_bp.route('/password', methods=['POST'])
@login_required
def update_password():
    """Change user password"""
    user_id = str(g.current_user['_id'])
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validate
    if not current_password or not new_password or not confirm_password:
        flash('All password fields are required', 'error')
        return redirect(url_for('settings.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('settings.profile'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters', 'error')
        return redirect(url_for('settings.profile'))
    
    # Change password
    success, error = change_password(user_id, current_password, new_password)
    
    if not success:
        flash(error, 'error')
        return redirect(url_for('settings.profile'))
    
    flash('Password changed successfully', 'success')
    return redirect(url_for('settings.profile'))


@settings_bp.route('/preferences', methods=['GET'])
@login_required
def preferences():
    """Display user preferences page"""
    user_id = str(g.current_user['_id'])
    prefs = get_user_preferences(user_id)
    
    return render_template('settings/preferences.html', preferences=prefs or {})


@settings_bp.route('/preferences', methods=['POST'])
@login_required
def update_preferences():
    """Update user preferences"""
    user_id = str(g.current_user['_id'])
    
    # Get preferences from form
    preferences = {
        'theme': request.form.get('theme', 'light'),
        'notifications': request.form.get('notifications', 'off') == 'on',
        'timezone': request.form.get('timezone', 'UTC'),
        'date_format': request.form.get('date_format', 'MM/DD/YYYY'),
        'currency': request.form.get('currency', 'USD')
    }
    
    # Update preferences
    updated_prefs, error = update_user_preferences(user_id, preferences)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('settings.preferences'))
    
    flash('Preferences saved successfully', 'success')
    return redirect(url_for('settings.preferences'))

