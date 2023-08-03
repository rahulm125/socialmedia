from flask_wtf import FlaskForm
from wtforms import (SubmitField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AddFriend(FlaskForm):
    friends = SelectField('Users',choices=[])
    addfrnd = SubmitField('Add Friend')