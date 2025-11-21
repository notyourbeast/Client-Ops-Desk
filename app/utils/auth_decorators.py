from functools import wraps

from bson import ObjectId
from flask import g, redirect, url_for, request

from app.repositories.db import get_db
from app.utils.jwt_utils import decode_token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return redirect(url_for('auth.login_form'))

        payload, error = decode_token(token)
        if error:
            return redirect(url_for('auth.login_form'))

        db = get_db()
        user = db.users.find_one({'_id': ObjectId(payload['user_id'])})
        if not user:
            return redirect(url_for('auth.login_form'))

        user.pop('password_hash', None)
        g.current_user = user

        return f(*args, **kwargs)
    return decorated_function

