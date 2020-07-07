from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    _id = db.Column('_id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.String(32), nullable=False)
    password = db.Column('pass', db.String(128), nullable=False)
    date_added = db.Column('date_added', db.DateTime, default=db.func.now())
    last_login = db.Column('last_login', db.DateTime, index=False, unique=False, nullable=True)
    last_login_attempt = db.Column('last_login_attempt', db.DateTime, index=False, unique=False, nullable=True)
    last_login_attempt_count = db.Column('last_login_attempt_count', db.Integer, index=False, unique=False, nullable=True)
    last_login_attempt_total = db.Column('last_login_attempt_total', db.Integer, index=False, unique=False, nullable=True)
    login_ban_dt = db.Column('login_ban_period', db.DateTime, index=False, unique=False, nullable=True)
    login_ban_period = db.Column('login_ban_period', db.TIMESTAMP, index=False, unique=False, nullable=True)
    login_ban_count = db.Column('login_ban_count', db.Integer, index=False, unique=False, nullable=True)
    login_verify = db.Column('login_verification_required', db.Boolean, index=False, unique=False, nullable=True)
    account_suspended = db.Column('account_suspended', db.Boolean, index=False, unique=False, nullable=True)

    @staticmethod
    def get_by_name(name):
        return db.Session.query(Users).filter_by(name=name).one()

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Content(db.Model):
    __tablename__ = "content"

    _id = db.Column('_id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(32), nullable=False)
    body = db.deferred(db.Column('body', db.Text))
    creator_id = db.Column('creator_id', db.Integer, db.ForeignKey('users._id'))
    date_added = db.Column('date_added', db.DateTime, default=db.func.now())


class Notes(db.Model):
    __tablename__ = "notes"

    _id = db.Column('_id', db.Integer, primary_key=True)
    from_id = db.Column('from_id', db.Integer, db.ForeignKey('users._id'))
    to_id = db.Column('to_id', db.Integer, db.ForeignKey('users._id'))
    title = db.Column('title', db.String(255), nullable=False)
    date_added = db.Column('date_added', db.DateTime, default=db.func.now())
    max_access_count = db.Column('max_access_count', db.Integer)
    max_access_attempts = db.Column('max_access_count', db.Integer)
    access_counter = db.Column('access_counter', db.Integer)
    access_attempts = db.Column('access_counter', db.Integer)
    content = db.Column('content', db.Integer, db.ForeignKey('content._id'))
    allow_anon = db.Column('content', db.Boolean)

    def add_note(self):
        return ''

    def show_note(self):
        return
