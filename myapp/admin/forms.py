from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, FileField, TextAreaField, RadioField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AdminSignUp(FlaskForm):
    user = StringField('User', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class AdminSignIn(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class WebSetting(FlaskForm):
    name = StringField('Website Name', validators=[DataRequired()])
    favicon = FileField('Favicon (16px*16px)')
    logo = FileField('Logo (60px*46px)')
    copyrights = StringField('Copyright', validators=[DataRequired()])
    lsliderone = StringField('Slider One Heading', validators=[DataRequired()])
    lonedesc = TextAreaField('Slider One Description', validators=[DataRequired(), Length(min=3, max=150)])
    lonephoto = FileField('Slider One Photo (600px*400px)')
    lslidertwo = StringField('Slider Two Heading', validators=[DataRequired()])
    ltwodesc = TextAreaField('Slider Two Description', validators=[DataRequired(), Length(min=3, max=150)])
    ltwophoto = FileField('Slider Two Photo (600px*400px)')
    lsliderthree = StringField('Slider Three Heading', validators=[DataRequired()])
    lthreedesc = TextAreaField('Slider Three Description', validators=[DataRequired(), Length(min=3, max=150)])
    lthreephoto = FileField('Slider Three Photo (573px*435px)')
    swebheading = StringField('Signup Page Heading', validators=[DataRequired()])
    sdesc = StringField('Signup Page Description', validators=[DataRequired()])
    lphoto = FileField('Admin Login&Signup Page Photo (500px*667px)')
    signup = RadioField('Admin Signup:', coerce=int ,choices=[(1,'On'), (0,'Off')])
    submit = SubmitField('Save Details')


# class WebSetting(FlaskForm):
#     name = StringField('Website Name', validators=[DataRequired()])
#     favicon = FileField('Favicon (16px*16px)')
#     logo = FileField('Logo (60px*46px)')
#     copyrights = StringField('Copyright', validators=[DataRequired()])
#     lsliderone = StringField('Slider One Heading', validators=[DataRequired()])
#     lonedesc = TextAreaField('Slider One Description', validators=[DataRequired(), Length(min=3, max=150)])
#     lonephoto = FileField('Slider One Photo (600px*400px)')
#     lslidertwo = StringField('Slider Two Heading', validators=[DataRequired()])
#     ltwodesc = TextAreaField('Slider Two Description', validators=[DataRequired(), Length(min=3, max=150)])
#     ltwophoto = FileField('Slider Two Photo (600px*400px)')
#     lsliderthree = StringField('Slider Three Heading', validators=[DataRequired()])
#     lthreedesc = TextAreaField('Slider Three Description', validators=[DataRequired(), Length(min=3, max=150)])
#     lthreephoto = FileField('Slider Three Photo (573px*435px)')
#     swebheading = StringField('Signup Page Heading', validators=[DataRequired()])
#     sdesc = StringField('Signup Page Description', validators=[DataRequired()])
#     lphoto = FileField('Admin Login&Signup Page Photo (500px*667px)')
#     signup = SelectField('Admin Signup:', choices=[('On'), ('Off')])
#     submit = SubmitField('Save Details')