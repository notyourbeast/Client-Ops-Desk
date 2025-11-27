from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, session, current_app
import requests

from app.services.auth_service import register_user, authenticate_user
from app.services.oauth_service import get_or_create_google_user
from app.utils.jwt_utils import create_token
from app.config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET'])
def register_form():
    return render_template('auth/register.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'name': request.form.get('name', '')
    }

    user, error = register_user(data)
    if error:
        flash(error, 'error')
        return redirect(url_for('auth.register_form'))

    flash('Registration successful. Please login.', 'success')
    return redirect(url_for('auth.login_form'))


@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user, error = authenticate_user(email, password)
    if error:
        flash(error, 'error')
        return redirect(url_for('auth.login_form'))

    # Store basic user info in session (for non-Google users, no picture available)
    session['user'] = {
        'name': user.get('name', ''),
        'email': user.get('email', ''),
        'picture': None
    }

    token = create_token(user['_id'], user['email'])
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('auth_token', token, httponly=True, secure=False, samesite='Lax', max_age=604800)

    return response


@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Clear session data including user profile
    session.clear()
    response = make_response(redirect(url_for('auth.login_form')))
    response.set_cookie('auth_token', '', httponly=True, expires=0)
    return response


@auth_bp.route('/google/login', methods=['GET'])
def google_login():
    """Initiate Google OAuth login"""
    google = current_app.config.get('GOOGLE_OAUTH')
    if not google:
        flash('Google OAuth is not configured. Please contact administrator.', 'error')
        return redirect(url_for('auth.login_form'))
    
    try:
        # Generate redirect URI using url_for to ensure it matches Flask's routing
        # This ensures consistency with the callback route
        redirect_uri = url_for('auth.google_callback', _external=True)
        
        # Log for debugging
        current_app.logger.info(f'OAuth redirect URI: {redirect_uri}')
        current_app.logger.info(f'Request host: {request.host}')
        current_app.logger.info(f'Request scheme: {request.scheme}')
        
        # Use authorize_redirect with explicit redirect_uri
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        current_app.logger.error(f'Error initiating Google OAuth: {str(e)}')
        flash('Failed to initiate Google login. Please try again.', 'error')
        return redirect(url_for('auth.login_form'))


@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    google = current_app.config.get('GOOGLE_OAUTH')
    if not google:
        flash('Google OAuth is not configured.', 'error')
        return redirect(url_for('auth.login_form'))
    
    try:
        # Check for error from Google
        error = request.args.get('error')
        if error:
            error_description = request.args.get('error_description', error)
            flash(f'Google authentication error: {error_description}', 'error')
            return redirect(url_for('auth.login_form'))
        
        # Authorize and get token
        # Authlib automatically extracts redirect_uri from the request, so don't pass it explicitly
        try:
            # Generate the redirect URI that should match what was sent
            expected_redirect_uri = url_for('auth.google_callback', _external=True)
            current_app.logger.info(f'Expected redirect URI: {expected_redirect_uri}')
            
            token = google.authorize_access_token()
        except Exception as token_error:
            current_app.logger.error(f'Token authorization error: {str(token_error)}')
            current_app.logger.error(f'Request args: {dict(request.args)}')
            flash(f'Failed to authorize with Google: {str(token_error)}', 'error')
            return redirect(url_for('auth.login_form'))
        
        if not token:
            flash('Failed to get access token from Google.', 'error')
            return redirect(url_for('auth.login_form'))
        
        # Get access token from the response
        # Token can be a dict with 'access_token' or just the token string
        if isinstance(token, dict):
            access_token = token.get('access_token')
        elif isinstance(token, str):
            access_token = token
        else:
            flash('Invalid token format from Google.', 'error')
            return redirect(url_for('auth.login_form'))
            
        if not access_token:
            flash('Failed to get access token from Google.', 'error')
            return redirect(url_for('auth.login_form'))
        
        # Get user info using requests directly with the full URL
        # Use the OpenID Connect userinfo endpoint (newer, more reliable)
        user_info_response = requests.get(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if user_info_response.status_code != 200:
            flash(f'Failed to get user info from Google: {user_info_response.status_code}', 'error')
            return redirect(url_for('auth.login_form'))
        
        user_info = user_info_response.json()
        
        google_user_data = {
            'email': user_info.get('email'),
            'name': user_info.get('name', ''),
            'sub': user_info.get('sub')
        }
        
        if not google_user_data.get('email'):
            flash('Email not provided by Google. Please try again.', 'error')
            return redirect(url_for('auth.login_form'))
        
        user, error = get_or_create_google_user(google_user_data)
        
        if error:
            flash(error, 'error')
            return redirect(url_for('auth.login_form'))
        
        # Store user profile info in session (name, email, picture)
        session['user'] = {
            'name': user_info.get('name', ''),
            'email': user_info.get('email', ''),
            'picture': user_info.get('picture', '')
        }
        
        token_jwt = create_token(user['_id'], user['email'])
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('auth_token', token_jwt, httponly=True, secure=False, samesite='Lax', max_age=604800)
        
        flash('Successfully signed in with Google!', 'success')
        return response
        
    except Exception as e:
        import traceback
        current_app.logger.error(f'Google OAuth error: {str(e)}\n{traceback.format_exc()}')
        flash(f'Google authentication failed: {str(e)}', 'error')
        return redirect(url_for('auth.login_form'))

