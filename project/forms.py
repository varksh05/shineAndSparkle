from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class CheckoutForm(FlaskForm):
    name = StringField('Billing Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',  validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=15, max=120)])
    submit = SubmitField('Place Order')

class LoginForm(FlaskForm):
    un = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    pw = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Login')
