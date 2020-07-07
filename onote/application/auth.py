from . import login_manager
from .forms import LoginForm
from . import db
from .models import Users
from . import utils
from .utils import Utils

from flask import current_app as app
from flask import session, flash, url_for
from flask import Blueprint
from flask import request, redirect, render_template
from flask_login import current_user, login_required, logout_user, login_user

from datetime import datetime

from .auth_handler import auth_schema_handler

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_schema_handler
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.form.html')

    if not form.is_submitted():
        return render_template('login.form.html', form=form)

    if not form.validate():
        form.login_errors.append('INVALID_FORM')
        return render_template('login.form.html', form=form)

    if session.get('login_require_captcha'):
        if not Utils.session().validate_captcha_request(form.session_id, form.captcha_answer):
            form.login_errors.append('CAPTCHA_ERROR')
            return render_template('login.form.html', form=form)

    user = Users.get_by_name(form.name)
    if user is None:
        form.login_errors.append('NON_EXISTENT_USER')
        return render_template('login.form.html', form=form)

    prev_login_attempt = user.last_login_attempt
    user.last_login_attempt = datetime.now()
    db.Session.commit()

    if user.login_ban_dt is not None:
        if datetime.now().timestamp() - user.login_ban_dt.timestamp() < user.login_ban_period:
            form.login_errors.append('LOGIN_BAN_PERIOD')
            return render_template('login.form.html', form=form)
        else:
            user.login_ban_dt = None
            db.Session.commit()

    if user.check_password(form.password):
        user.last_login_attempt_count = 0
        user.last_login_attempt = None
        user.login_ban_dt = None
        user.login_ban_period = None
        user.login_ban_count = None
        db.Session.commit()

        if session['login_verify_user'] == user.name:
            session['login_require_verify'] = True
            return redirect('/verify', 400)

        if not form.remember_me == True:
            form.remember_me = False

        login_user(user, False if not form.remember_me == True else True)

        if session.get('login_require_action'):
            action = session.pop('login_require_action')
            return redirect(action, 400)
        else:
            return redirect('/dashboard', 400)

    form.login_errors.append('WRONG_PASSWORD')

    if prev_login_attempt is not None:
        if user.last_login_attempt.timestamp() - prev_login_attempt() < app.config['login_attempt_min_interval']:
            form.login_errors.append('TOO_SHORT_LOGIN_INTERVAL')
            user.last_login_attempt_count += 1
            user.last_login_attempt_total += 1
            if Utils.captcha_enabled and user.last_login_attempt_total > app['login_attempts_captcha_threshold']:
                session['login_require_captcha'] = True

            if user.last_login_attempt_count > app.config['last_login_attempt_threshold']:
                user.last_login_attempt_count = 0
                if user.login_ban_count is None:
                    user.login_ban_count = 1
                    if user.login_ban_count > app.config['login_ban_period_max_multiply']:
                        user.login_ban_count = 1
                        if user.last_login_attempt_total > app['login_attempts_verify_threshold']:
                            user.login_verify = True
                            session['login_verify_user'] = user.name
                            session['remember_me'] = form.remember_me
                            db.Session.commit()
                            return redirect('/verify')
                    user.login_ban_count = datetime.now()
                    user.login_ban_dt = datetime.now()
                    user.login_ban_period = app.config['login_ban_period_base'] + (app.config['login_ban_period_multiplier'] * user.login_ban_count)
                    form.login_errors.append('LOGIN_BAN_PERIOD')
                    db.Session.commit()
                    return render_template('login.form.html', form=form)
        return render_template('login.form.html', form=form)


@auth_schema_handler
@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    session.pop('login_require_verify')
    user = Users.get_by_name(session['login_require_verify'])
    session.pop('login_verify_user')
    login_user(user, session['remember_me'])
    session.pop('remember_me')

    if session.get('login_require_action'):
        action = session.pop('login_require_action')
        return redirect(action, 400)
    else:
        return redirect('/dashboard', 400)


@auth_schema_handler
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return "FUCK"
    # Signup logic goes here


@auth_schema_handler
@auth_bp.route('/cancel', methods=['GET', 'POST'])
def signup():
    return "FUCK"
    # Signup logic goes here


@auth_schema_handler
@auth_bp.route('/destroy', methods=['GET', 'POST'])
def signup():
    return "FUCK"
    # Signup logic goes here


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return db.User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))