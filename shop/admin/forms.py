from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=45)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, max=60)
    ])
    confirm = PasswordField('Repeat Password')
