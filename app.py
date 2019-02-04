from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from config import Config
from flask_blogging import BloggingEngine, SQLAStorage
from models import Post, Tags, Admin
from forms import PostEdit, LoginForm
from start import app, db
from flask_login import login_user, login_required, current_user
from flask import request
from werkzeug.urls import url_parse

"""
app = Flask(__name__)

app.config.from_object(Config)
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db.init_app(app)
engine = db.get_engine()
tables = db.get_tables_for_bind()
db.make_connector()

migrate = Migrate(app, db)

# code for the blogging app
#storage = SQLAStorage(db)
"""


# General variables to be used across all pages
site_components = ['Home', 'Blog', 'About']

@app.route('/')
def home():
    text = 'The home page will contain initiatives, links to the blog, coding progress, etc.'
    return render_template('home.html', text = text, site_components = site_components)

@app.route('/blog/')
def blog():
    text = "The place where I will record my development progress and write down my thoughts"
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog.html', text = text, site_components = site_components, posts=posts)

@app.route('/about/')
def about():
    text = 'This website was eniterly written by me using Python. It is deployed on Google Cloud Platform.'
    return render_template('about.html', text = text, site_components = site_components)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('admin_page')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
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
