import os, json
from google.cloud import storage
basedir = os.path.abspath(os.path.dirname(__file__))

client = storage.Client()
bucket = client.get_bucket('craigstanton2.appspot.com')
creds = bucket.get_blob('creds.json').download_as_string()
data = json.loads(creds)


class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
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







