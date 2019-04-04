from flask import Flask, render_template, flash, redirect, url_for, request, Response, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, datetime
from config import Config
from flask_blogging import BloggingEngine, SQLAStorage
#from models import Post, Tags, Admin
from forms import PostEdit, LoginForm
from mysite import app, oauth2
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.urls import url_parse


from general_functions.datastore.datastore import *

# General variables to be used across all pages
site_components = ['Home', 'Blog', 'About']

@app.route('/')
def home():
    text = 'The home page will contain initiatives, links to the blog, coding progress, etc.'
    return render_template('home.html', text = text, site_components = site_components)

@app.route('/blog/')
def blog():
    text = "The place where I will record my development progress and write down my thoughts"
    posts = blog_list()
    return render_template('blog.html', text = text, site_components = site_components, posts=posts)

@app.route('/about/')
def about():
    text = 'This website was eniterly written by me using Python. It is deployed on Google Cloud Platform.'
    return render_template('about.html', text = text, site_components = site_components)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    if oauth2.email == 'craig.stanton2@gmail.com':
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
    """
    next_page = url_for('admin_page')
    return redirect(next_page)
    #return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    oauth2.storage.delete()
    return redirect(url_for('home'))

@app.route('/admin/', methods=['GET', 'POST'])
@oauth2.required
def admin_page():
    if oauth2.email == 'craig.stanton2@gmail.com':
        hasauth = oauth2.has_credentials()
        form = PostEdit()
        if form.validate_on_submit():
            #way to get date posted to merge with file
            print(request.form['date_posted'])
            
            data = request.form.to_dict(flat=True)
            if request.files:
                data['post_filename'] = request.form['date_posted'].replace(" ", "-").replace(":", "-") + "_" + request.files['post_file'].filename
                file_upload(request.files['post_file'], request.form['date_posted'])
            
            update(data)

            return redirect(url_for('blog'))
    else:
        #flash('Invalid username or password')
        return redirect(url_for('blog'))
    return render_template('admin.html', form=form, hasauth=hasauth)


@app.route('/blog/<post_filename>')
def display_blog_post(post_filename):
    blog_detail = get_file(post_filename)
    return render_template('blog_detail.html', blog_detail = blog_detail, site_components = site_components)


if __name__ == '__main__':
    app.run()
