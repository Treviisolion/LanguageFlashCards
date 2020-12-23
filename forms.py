from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    """Form for logging in and creating users"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LanguageForm(FlaskForm):
    """Form for adding new languages"""

    language = StringField('Language', validators=[DataRequired(), Length(max=3)])