import os, json
basedir = os.path.abspath(os.path.dirname(__file__))

with open('app.json') as f:
    data = json.load(f)

class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://Craig:Spurs2018!@localhost/craigstanton2.0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH2_CLIENT_ID = \
    data['gae_oauth2']['client_id']
    GOOGLE_OAUTH2_CLIENT_SECRET = data['gae_oauth2']['client_secret']
    SECRET_KEY = data['flask_general']['secret_key']

class ProductionConfig(Config):
    DEBUG = False
    CSRF_ENABLED = True
    DATA_BACKEND = 'datastore'
    GOOGLE_OAUTH2_CLIENT_ID = \
    data['gae_oauth2']['client_id']
    GOOGLE_OAUTH2_CLIENT_SECRET = data['gae_oauth2']['client_secret']
    SECRET_KEY = data['flask_general']['secret_key']
    PROJECT_ID = 'craigstanton2'

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True







