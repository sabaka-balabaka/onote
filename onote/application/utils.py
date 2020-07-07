import flask
from flask import Blueprint
from flask import render_template
from flask import current_app as app
from flask import session, abort
import random
from . import captcha
from datetime import datetime

RND_STR='A-Za-z0-9'


def rnd_str(l=64):
    if l > len(RND_STR):
        return random.shuffle(RND_STR)[0:len(RND_STR)-1] + rnd_str(l-len(RND_STR))
    return random.shuffle(RND_STR)[0:l-1]


class BruteforceEx(Exception):
    pass


class CaptchaEx(Exception):
    pass


class InactivityEx(Exception):
    pass


class FraudEx(Exception):
    pass


class Utils:
    def __init__(self):
        self._id = rnd_str()
        self._captcha_img = captcha.generate()
        self._captcha_text = captcha.get_answer()
        self._captcha_key = rnd_str()
        self._captcha_attempts = 0
        self._last_captcha_attempt = datetime.now().timestamp()
        self._last_captcha_refresh = datetime.now().timestamp()
        self._prev_captcha_attempt = datetime.now().timestamp()
        self._last_used = datetime.now().timestamp()

    def validate_captcha(self, session_id, captcha_text):
        self._captcha_attempts += 1
        if self._captcha_attempts > app.config['CAPTCHA_ATTEMPTS_THRESHOLD']:
            session.clear()
            raise CaptchaEx()

        self._prev_captcha_attempt = self._prev_captcha_attempt
        self._last_captcha_attempt = datetime.now().timestamp()
        if self._last_captcha_attempt - self._prev_captcha_attempt < app.config['CAPTCHA_ATTEMPT_INTERVAL']:
            return False

        if self._id == session_id and self._captcha_text == captcha_text:
            self._captcha_img = None
            self._captcha_text = None
            return self._captcha_key
        return None

    def validate_captcha_request(self, session_id, captcha_key):
        if self._id == session_id and self._captcha_key == captcha_key:
            self._captcha_key = None
            return True

        session.clear()
        raise BruteforceEx()

    def refresh_captcha(self):
        if datetime.now().timestamp() - self._last_captcha_refresh < app.config['CAPTCHA_REFRESH_INTERVAL_MIN']:
            return False

        self._captcha_img = captcha.generate()
        self._captcha_text = captcha.get_answer()
        self._last_captcha_refresh = datetime.now().timestamp()
        return True

    @property
    def captcha_img(self):
        return self._captcha_img

    @property
    def captcha_enabled(self):
        if not app.config.get('CAPTCHA_ENABLED'):
            return False
        if not app.config['CAPTCHA_ENABLED'].lower() == 'yes':
            return False
        return True

    def use(self):
        dt = datetime.now.timestamp()
        if dt - self._last_used > app.config['onote_inactivity_timeout']:
            session.clear()
            raise InactivityEx()

        self._last_used = dt
        return True

    @staticmethod
    def init_session():
        session['utils'] = Utils()

    @staticmethod
    def session():
        return session.get('utils')


errors_bp = Blueprint('errors', __name__)


@errors.app_errorhandler(BruteforceEx)
def handle_bruteforce_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False

    return render_template('bruteforce.error.html')


@errors.app_errorhandler(CaptchaEx)
def handle_bruteforce_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False

    return render_template('captcha.error.html')


@errors.app_errorhandler(InactivityEx)
def handle_bruteforce_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False

    return render_template('inactivity.error.html')


@errors.app_errorhandler(FraudEx)
def handle_bruteforce_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False

    return render_template('fraud.error.html')