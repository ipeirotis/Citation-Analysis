from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, validators

from flask import session
from wtforms.meta import DefaultMeta
from wtforms.csrf.session import SessionCSRF

from main import app

class BaseForm(Form):
    class Meta(DefaultMeta):
        csrf = app.config['CSRF_ENABLED']
        csrf_class = SessionCSRF
        csrf_secret = app.config['SECRET_KEY']

        @property
        def csrf_context(self):
            return session

class AuthorForm(BaseForm):
    authorId = StringField('Author ID', [validators.Required()])
    submit = SubmitField("Search")
