import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Set the SECRET_KEY to a random value.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    # Set the SQLALCHEMY_DATABASE_URI. If the DATABASE_URL is not set, use a SQLite database by default.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Set the SQLALCHEMY_TRACK_MODIFICATIONS to False to improve the performance.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Set the email settings for the mail server.
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_PORT = 465
    MAIL_USERNAME = "924082621@qq.com"
    MAIL_PASSWORD = "vyiubszzwbojbdic"
    MAIL_DEFAULT_SENDER = "924082621@qq.com"