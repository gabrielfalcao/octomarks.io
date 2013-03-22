from flask.ext.wtf import (
    Form, IntegerField, TextField, PasswordField, validators,
)


class SignupForm(Form):
    business_id = IntegerField('business_id', [validators.Required()])
    first_name = TextField('first_name', [validators.Required()])
    last_name = TextField('last_name', [validators.Required()])

    email = TextField('eMail', [validators.Required()])
    password = PasswordField(
        'Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Confirm Password', [validators.Required()])
