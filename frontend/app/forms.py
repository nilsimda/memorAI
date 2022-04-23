from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    birth_year = StringField('Birth Year', validators=[DataRequired()])
    birth_place = StringField('Birth Place (Country)', validators=[DataRequired()])
    current_place = StringField('Current Place (Country)', validators=[DataRequired()])
    favorite_film = StringField('Favorite Film', validators=[DataRequired()])
    favorite_band = StringField('Favorite Band', validators=[DataRequired()])
    submit = SubmitField('Register')

