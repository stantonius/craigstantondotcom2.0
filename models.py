from mysite import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

subs = db.Table('subs',
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'))
    )


class Post(db.Model):

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(25), nullable=False)
    post_tags = db.relationship('Tags', secondary=subs, backref=db.backref('posts', lazy='dynamic'))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # placeholder for JSON (jsonb type in psql) for comments, etc

    def __repr__(self):
        return '<Post {}'.format(self.title)


class Tags(db.Model):

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag_name)


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
