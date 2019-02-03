from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from config import Config
from flask_blogging import BloggingEngine, SQLAStorage
from models import *
from forms import PostEdit

app = Flask(__name__)

app.config.from_object(Config)
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
engine = db.get_engine()
tables = db.get_tables_for_bind()
db.make_connector()

migrate = Migrate(app, db)

# code for the blogging app
#storage = SQLAStorage(db)
blogging_engine = BloggingEngine(app, db)

# General variables to be used across all pages
site_components = ['Home', 'Blog', 'About']

@app.route('/')
def home():
    text = 'The home page will contain initiatives, links to the blog, coding progress, etc.'
    return render_template('home.html', text = text, site_components = site_components)

@app.route('/blog/')
def blog():
    text = "The place where I will record my development progress and write down my thoughts"
    posts = Post.query.all()
    return render_template('blog.html', text = text, site_components = site_components, posts=posts)

@app.route('/about/')
def about():
    text = 'Content about me and what my goals are'
    return render_template('about.html', text = text, site_components = site_components)

@app.route('/admin/', methods=['GET', 'POST'])
def admin_page():
    form = PostEdit()
    if form.validate_on_submit():
        post = Post(
            title=form.post_title.data,
            subtitle=form.post_subtitle.data,
            author=form.author.data,
            #post_tags="Need to fix",
            content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Post titled "{}" has been created'.format(form.post_title.data))
        return redirect(url_for('blog'))
    return render_template('admin.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
