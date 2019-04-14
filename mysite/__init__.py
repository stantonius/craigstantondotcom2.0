from flask import Flask
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
import socket
from flask_ckeditor import CKEditor
import warnings
import datetime

from oauth2client.contrib.flask_util import UserOAuth2

warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")



app = Flask(__name__, static_folder='static')

ckeditor = CKEditor(app)
#admin = Admin(app, name='microblog', template_mode='bootstrap3')

if socket.gethostname() == 'Chizzler':
        app.config.from_object(Config)
else:
        app.config.from_object(ProductionConfig)

oauth2 = UserOAuth2()

oauth2.init_app(
        app,
        scopes=['email', 'profile'])

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    format=r"%d %B %Y"
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(format)
