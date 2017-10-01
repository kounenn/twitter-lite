from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    content = TextAreaField("Say some thing", validators=[DataRequired(),
                                                          Length(1, 140)])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Name:', validators=[Length(4, 64)])
    location = StringField('Location', validators=[Length(max=64)])
    about_me = TextAreaField('About me:', validators=[Length(max=1024)])
    submit = SubmitField('Submit')
