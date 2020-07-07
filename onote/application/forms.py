from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    name = StringField('name', id='name',
                       validators=[InputRequired(message='EMPTY_USER_NAME'),
                                   Regexp("^[a-zA-Z]{1}[a-zA-Z0-9]{1,31}$", message='INVALID_USER_NAME'),
                                   Length(min=6, max=32, message='IVALID_USER_NAME_LENGTH')])
    password = PasswordField('password', id='password',
                             validators=[InputRequired(message='EMPTY_USER_NAME'),
                                         Length(min=6, max=32, message='IVALID_PASSWORD_LENGTH'),
                                         Regexp("^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$", message='INVALID_PASSWORD')])
    remember_me = BooleanField('remember_me', id='remember-me')
    submit = SubmitField('submit', id='submit')
    session_id = HiddenField('session_id')
    captcha_key = HiddenField('captcha_key')

    login_errors = list()
