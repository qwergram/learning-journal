from wtforms import Form, StringField, TextAreaField, validators, HiddenField
from wtforms import HiddenField


def strip_filter(x):
    """Remove excess whitespace around input text"""
    return x.strip() if x else None


class EntryCreateForm(Form):
    title = StringField('title', [validators.Length(min=1, max=128)],
                        filters=[strip_filter])
    text = TextAreaField('text', [validators.Length(min=1)],
                         filters=[strip_filter])


class EntryUpdateForm(EntryCreateForm):
    id = HiddenField()


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=1, max=16)])
    password = StringField('password', [validators.Length(min=1, max=16)])
