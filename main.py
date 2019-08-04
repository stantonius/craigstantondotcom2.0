from flask import Flask, render_template, flash, redirect, url_for, request, Response, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, datetime
from forms import PostEdit, LoginForm
from mysite import app, oauth2
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.urls import url_parse
import folium

from util.datastore.datastore import *
from util.apps.traveller_map import *

# General variables to be used across all pages
site_components = ['Home', 'Blog', 'About', 'Apps']
allowed_ids = ["craig.stanton2@gmail.com"]

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
    text = ""
    return render_template('about.html', text = text, site_components = site_components)

@app.route('/apps/')
def apps():
    list_of_apps = ["traveller", "pygame"]
    text = "Series of experimental apps"
    return render_template('apps.html', text = text, list_of_apps = list_of_apps, site_components = site_components)

@app.route('/apps/traveller')
def traveller():
    text = "These are all of the countries I have travelled to. The purpose of this was to deploy a simple app using Google Cloud Functions."
    return render_template('traveller.html', text = text, site_components = site_components)

@app.route('/apps/pygame')
def pygame():
    text = "In development. Plase come back soon!"
    return render_template('pygame.html', text = text, site_components = site_components)

#NOTE: Below is just used to render the map - it is not a dedicated webpage itself
@app.route('/apps/map')
def map():
    text = mapper()
    m = folium.Map(location=[41.0082, 20], zoom_start=1.5, min_zoom=2)
    folium.Choropleth(geo_data=text,
                      fill_color='red',
                      fill_opacity=0.3,
                      line_weight=2,
                     ).add_to(m)
    return m.get_root().render()

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = url_for('admin_home')
    return redirect(next_page)

@app.route('/logout')
def logout():
    oauth2.storage.delete()
    return redirect(url_for('home'))

@app.route('/admin/new_post/', methods=['GET', 'POST'])
@oauth2.required
def new_post():
    if oauth2.email in allowed_ids:
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
    return render_template('new_post.html', form=form, hasauth=hasauth)


@app.route('/<id>/edit', methods=['GET', 'POST'])
@oauth2.required
def edit(id):
    if oauth2.email in allowed_ids:
        post = read(id)
        form = PostEdit()
        form.post_title.data = post['post_title']
        form.post_subtitle.data = post["post_subtitle"]
        form.author.data = post["author"]
        form.content.data = post["content"]
        form.post_tags.data = post["post_tags"]
           
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            if not request.files and "post_filename" in post:
                data["post_filename"] = post["post_filename"]
            elif request.files:
                data['post_filename'] = request.form['date_posted'].replace(" ", "-").replace(":", "-") + "_" + request.files['post_file'].filename
                file_upload(request.files['post_file'], request.form['date_posted'])
            update(data, id)
            return redirect(url_for('admin_home'))
    else:
        #flash('Invalid username or password')
        return redirect(url_for('blog'))

    return render_template("new_post.html", form=form)


@app.route('/admin/', methods=['GET', 'POST'])
@oauth2.required
def admin_home():
    if oauth2.email in allowed_ids:
        posts = blog_list()
    else:
        #flash('Invalid username or password')
        return redirect(url_for('blog'))
    return render_template('admin.html', site_components = site_components, posts=posts)


@app.route('/blog/<post_filename>')
def display_blog_post(post_filename):
    blog_detail = get_file(post_filename)
    return render_template('blog_detail.html', blog_detail = blog_detail, site_components = site_components)


if __name__ == '__main__':
    app.run()
