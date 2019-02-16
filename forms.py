from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectMultipleField, FileField
from wtforms.ext.sqlalchemy.orm import QuerySelectMultipleField
from wtforms.validators import DataRequired
import datetime

choices = [('AI', 'AI'), ('random_thoughts', 'Random Thoughts'), ('microcomputing', 'Microcomputing')]

class PostEdit(FlaskForm):
    post_title = StringField('Title', validators=[DataRequired()])
    post_subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Post content', validators=[DataRequired()])
    date_posted = DateTimeField('Date posted', default=datetime.datetime.utcnow(), format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    post_tags = SelectMultipleField('Tags', choices=choices, validators=[DataRequired()])
    save_draft = BooleanField('Save as draft')
    submit = SubmitField('Post')
    post_file = FileField('Post Markdown')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
