class Config(object):
    DEBUG = True
    SECRET_KEY = b'\xb9,\x01\xa6\xb7[(\xae\xe9>\xe8.-\xfb\x11bg;\xa4\xe0Le4\xa8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:onote@172.23.0.2:3306/onote'
    SESSION_TYPE = 'sqlalchemy'
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 5
    CAPTCHA_WIDTH = 160
    CAPTCHA_HEIGHT = 60