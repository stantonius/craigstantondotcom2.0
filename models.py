from app import db

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
