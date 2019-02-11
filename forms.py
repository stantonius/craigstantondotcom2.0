from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.orm import QuerySelectMultipleField
from wtforms.validators import DataRequired

class PostEdit(FlaskForm):
    post_title = StringField('Title', validators=[DataRequired()])
    post_subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    tags = QuerySelectMultipleField('Tags')
    content = TextAreaField('Post content', validators=[DataRequired()])
    save_draft = BooleanField('Save as draft')
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
