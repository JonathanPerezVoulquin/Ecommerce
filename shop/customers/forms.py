from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from flask_wtf.file import FileRequired, FileAllowed, FileField

class CustomerRegisterForm(Form):
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

