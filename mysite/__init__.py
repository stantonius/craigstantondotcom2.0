from flask import Flask
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import socket

from oauth2client.contrib.flask_util import UserOAuth2

app = Flask(__name__, static_folder='static')

if socket.gethostname() == 'Chizzler':
        app.config.from_object(Config)
else:
        app.config.from_object(ProductionConfig)

oauth2 = UserOAuth2()

oauth2.init_app(
        app,
        scopes=['email', 'profile'])