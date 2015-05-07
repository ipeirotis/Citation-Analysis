"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
app = Flask('CitationAnalysis')
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import settings
app.config.from_object(settings.Development)

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from flask import request, render_template, flash, url_for
from forms import AuthorForm

@app.route('/', methods=['GET', 'POST'])
def index():
    """Index page."""
    form = AuthorForm(request.form)
    results = None
    if form.validate_on_submit():
        results = "The author ID was: %s" % form.authorId.data
        # HERE THE AUTHOR CRAWLER SHOULD BE CALLED INSTEAD
    return render_template('index.html', form=form, action=url_for('index'),
                           results=results)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
