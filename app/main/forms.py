from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField, RadioField
from wtforms.validators import Required


class BlogForm(FlaskForm):
    category_id = SelectField('Select Category', choices=[('1', 'Fashion Blogs'), ('2', 'Food Blogs'), ('3', 'Travel Blogs'),('4','Music Blogs'),('5','Lifestyle Blogs')])
    content = TextAreaField('YOUR BLOG')
    submit = SubmitField('SUBMIT')

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('SUBMIT')



class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')