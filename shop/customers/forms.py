from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name:')
    username = StringField('Username:', [validators.DataRequired()])
    email = StringField('Email:', [validators.Email(), validators.DataRequired()])
    password= PasswordField('Password:',[validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match!')])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    country = StringField('Country:', [validators.DataRequired()])
    province = StringField('Province:', [validators.DataRequired()])
    city = StringField('City:', [validators.DataRequired()])
    postal_code = StringField('Postal Code:', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])
    contact = StringField('Contact', [validators.DataRequired()], render_kw={"placeholder": "+54"})

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

    submit = SubmitField('Register')


    def validate_username(self, username):
        if Register.query.filter_by(username=username.data):
            raise ValidationError('This username is alredy in use, please select other')

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data):
            raise ValidationError('This email is alredy in use, please select other', 'success')


class CustomerLoginForm(FlaskForm):
    email = StringField('Email:', [validators.Email(), validators.DataRequired()])
    password= PasswordField('Password:',[validators.DataRequired()])