import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # Flags
    DEBUG = True
    TESTING = False

    # Creds
    MTA_API_KEY = os.getenv('MTA_API_KEY')

    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
