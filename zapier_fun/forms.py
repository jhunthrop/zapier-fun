from wtforms import Form, StringField, validators
from wtforms.fields.html5 import EmailField


class IntroduceForm(Form):

    first_name = StringField('First Name', [
        validators.InputRequired(),
        validators.Length(
            max=50,
            message="Wow, that's a long name. I don't trust you.")
    ])
    last_name = StringField('Last Name', [
        validators.InputRequired(),
        validators.Length(
            max=50,
            message="Wow, that's a long name. I don't trust you.")
    ])
    email = EmailField('Email', [
        validators.InputRequired(), validators.Email()
    ])
