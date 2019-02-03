from flask_caching import Cache
from flask_blogging import BloggingEngine

from app import app, db

blogging_engine = BloggingEngine(app, db)

engine = app.extensions["blogging"]
