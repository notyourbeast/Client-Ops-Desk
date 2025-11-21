from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash

from app.services.auth_service import register_user, authenticate_user
from app.utils.jwt_utils import create_token

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

    token = create_token(user['_id'], user['email'])
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('auth_token', token, httponly=True, secure=False, samesite='Lax', max_age=604800)

    return response


@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('auth.login_form')))
    response.set_cookie('auth_token', '', httponly=True, expires=0)
    return response

