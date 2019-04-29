from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField, RadioField
from wtforms.validators import Required

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('SUBMIT')

class PostForm(FlaskForm):
    title = StringField('Title',validators[DataRequired()])
    content = TextAreaField('Content',validators[DataRequired()]))
    submit = SubmitField('Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')