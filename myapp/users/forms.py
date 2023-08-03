from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, IntegerField, RadioField,
                     FileField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Regexp
from wtforms_validators import AlphaNumeric
from markupsafe import Markup

def years(start, end):
    lst1 = []
    for i in range(start, end):
        lst1.append(i)
    return lst1


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    date = IntegerField('Date', validators=[DataRequired(), NumberRange(min=1, max=31, message="Enter Valid Date")])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20, message='Username must be min 5 to max 20 characters!')])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'), ('Other','Other')])
    submit = SubmitField('SignUp')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SignIn')


class BasicProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    dob = StringField('Date of Birth')
    desc = TextAreaField('Description', validators=[DataRequired(), Length(min=3, max=300)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[Email()])
    gender = StringField('Genders')
    profile = FileField('Profile Photo')
    cover = FileField('Cover Photo')
    facebook = StringField('Facebook Profile')
    instagram = StringField('Instagram Profile')
    submit = SubmitField('Save Changes')

# class ProfilePhotoForm(FlaskForm):
#
#     submit = SubmitField('Save Changes')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Length(min=3, max=40)])
    submit_value = Markup('<i class="icofont-search"></i>')
    submit = SubmitField(submit_value)


class NewPostForm(FlaskForm):
    files = FileField('Photo/Video')
    desc = TextAreaField('Description')
    ptype = RadioField('Share With:', coerce=int, choices=[(1,'Only Friends'), (0,'Public')])
    submit = SubmitField('Publish')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[Length(min=2, max=198)])
    submit = SubmitField('Comment')



