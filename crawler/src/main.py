"""`main` is the top level module for your Flask application."""

import fix_path

# Import the Flask Framework
from flask import Flask
app = Flask('CitationAnalysis')
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

#Import authorCrawler
import authorCrawler

import settings
app.config.from_object(settings.Development)

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from flask import request, render_template, flash, url_for, redirect
from forms import AuthorForm, BaseForm

import MySQLdb


_db_host = '173.194.242.182'
_db_user = 'programize2'
_db_pass = 'scholar123!'
_db_unix_socket = '/cloudsql/citation-analysis:sql'


@app.route('/', methods=['GET', 'POST'])
def index():
    """Index page."""

    form = AuthorForm()
    retrieve_form = BaseForm()
    return render_template('index.html', form=form, retrieve=retrieve_form,
                           action=url_for('retrieve_author_data'),
                           retrieve_act=url_for('retrieve_author_data'))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


@app.route('/author', methods=['POST'])
@app.route('/author/<author_id>', methods=['GET'])
def retrieve_author_data(author_id=None):
    """Read authors' data saved in the database or
    fetch new data from the Google Scholar API.
    """
    if request.method == "POST":
        form = AuthorForm(request.form)
        if form.validate_on_submit():
            author = form.authorId.data
            author_obj = authorCrawler.authorCrawler(author, 3)
            flash(u"Author %s was successfully stored in the database." %
                  author_obj.name, 'success')
            return redirect(url_for('index'))

    elif author_id is None:
        return "Not found.", 404  # it should never arrive here

    else:
        db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                             user=_db_user, passwd=_db_pass)
        cursor = db.cursor()
        cursor.execute('USE scholar_db;')
        cursor.execute(
            (
                'select `authors`.name, `authors`.total_citations '
                'from `authors` '
                'where `authors`.author_id = %s;'
            ), (author_id,)
        )

        db.commit()
        author = cursor.fetchone()
        return render_template('show_authors.html', author=author,
                               act=url_for('index', _external=True))
