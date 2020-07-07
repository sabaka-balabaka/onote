from functools import wraps
from flask import session, redirect, url_for, request
from flask_login import current_user


def auth_shema_handler_api(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if session.get('account_suspended'):
            return '300 AUTH'
        if session.get('login_require_action'):
            if not (session.get('login_allow_signup') and
                    session.get('signup') and request.url_rule == url_for('signup')):
                return '300 AUTH'
        if session.get('login_require_verify'):
            return '300 AUTH'
        if session.get('login_require_otp'):
            return '300 AUTH'

        return f(*args, **kwds)
    return wrapper


def auth_schema_handler(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if session.get('account_suspended'):
            return redirect(url_for('suspended'))
        if session.get('login_require_action'):
            if not (session.get('login_allow_signup') and
                    session.get('signup') and request.url_rule == url_for('signup')):
                return redirect(url_for('login'))
        if session.get('login_require_verify'):
            return redirect(url_for('verify'))
        if session.get('login_require_otp'):
            return redirect(url_for('otp'))

        return f(*args, **kwds)
    return wrapper


def login_require_action(f, allow_signup=True):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user is None:
            session['login_require_action'] = request.url
            session['login_allow_signup'] = allow_signup
            return redirect(url_for('login'))

        return auth_schema_handler(f(*args, **kwds))
    return wrapper
