"""`main` is the top level module for your Flask application."""
import fix_path

# Import the Flask Framework
from flask import Flask
app = Flask('CitationAnalysis')
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
from google.appengine.api import taskqueue

#Import authorCrawler
import authorCrawler
import publicationCrawler

import settings
app.config.from_object(settings.Development)

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from flask import request, render_template, flash, url_for, redirect, jsonify
from forms import AuthorForm, BaseForm

import MySQLdb
import datetime
import urllib, urllib2, cookielib, traceback
from lxml import html
from lxml.etree import tostring

from google.appengine.api import urlfetch


# fetch deadline 45 seconds (just to be sure)
urlfetch.set_default_fetch_deadline(45)

_db_host = '173.194.242.182'
_db_user = 'programize2'
_db_pass = 'scholar123!'
_db_unix_socket = '/cloudsql/citation-analysis:sql'

CACHE_TTL = 30  # 30 days for a record to be considered old


@app.route('/', methods=['GET', 'POST'])
def index():
    """Index page."""

    ### below test for headers
    '''
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    url = "http://www.softlab.ntua.gr/~nickie/tmp/headers.php"
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36')]
    opener.open(url)
    f = opener.open(url)
    doc = html.parse(f)
    print (tostring(doc, pretty_print=True, method="html"))
    return 'OK', 200
    '''


    init_db()
    form = AuthorForm()
    retrieve_form = BaseForm()
    return render_template('index.html', form=form, retrieve=retrieve_form,
                           action=url_for('fetch_author_data'),
                           retrieve_act='/author')



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


@app.route('/fetchauthor', methods=['POST'])
def fetch_author_data():
    """Read authors' data saved in the database (if cached) or
    fetch new data from the Google Scholar API.
    """
    form = request.form
    try:
        author = form['authorId']
    except KeyError:
        return "Bad request", 400

    #include next line in /crawlauthor
    author_obj = authorCrawler.authorCrawler(author, 3)

    '''
    q_auth = taskqueue.Queue('AuthorsQueue')
    task = taskqueue.Task(url='/crawlAuthor', params={'authorId': author})
    q_auth.add(task)
    '''

    return "OK", 200
    #return redirect("/author/%s" % author)


'''
@app.route('/crawlAuthor', methods=['POST'])
def crawl_author():
    form = request.form
    try:
        author = form['authorId']
    except KeyError:
        return "Bad request", 400
    author_obj = authorCrawler.authorCrawler(author, 3)
'''


@app.route('/author/<author_id>', methods=['GET'])
def retrieve_author_data(author_id):
    if author_id is None:
        return "Not found.", 404  # it should never arrive here
    else:
        db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                             user=_db_user, passwd=_db_pass)
        #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

        cursor = db.cursor()
        try:
            cursor.execute('USE scholar_db;')
        except:
            init_db()
            cursor.execute('USE scholar_db;')

        cursor.execute(
            (
                'select `authors`.*, `coauthors`.coauthor_id '
                'from `authors` '
                'left join `coauthors` on `coauthors`.authors_author_id = '
                    '`authors`.author_id '
                'where `authors`.author_id = %s;'
            ), (author_id,)
        )

        db.commit()
        author_data = cursor.fetchall()
        if author_data:
            # fetch author's publication IDs

            form = request.form
            author = author_id

            try:
                nocache = request.args.get('nocache')
            except:
                nocache = None

            if nocache and nocache != "yes" and nocache != "no":
                return "Bad request.", 400

            if nocache == "yes":
                print('Must be refetched from Scholar')

                cursor.execute(
                            ('delete from `authors` where author_id = %s;'), (author_id,)
                )
                db.commit()

                url = url_for('fetch_author_data', _external=True)
                data = urllib.urlencode({ 'authorId': author_id })
                req = urllib2.Request(url, data)

                try:
                    response = urllib2.urlopen(req, timeout=600)
                except urllib2.HTTPError as e:
                    db.close()
                    return e.read(), int(e.code)
                else:
                    db.close()
                    #return redirect('/author/%s' % author_id)
                    return 'waiting for author to be fetched, retry later', 200

            if not nocache or nocache == "no":
                # if nocache is not present, then just check whether the record is old
                # (30 days default)


                cursor.execute(
                    (
                        'select last_time_retrieved '
                        'from `authors` '
                        'where `authors`.author_id = %s;'
                    ), (author,)
                )

                db.commit()

                last_time_retrieved = cursor.fetchone()
                if last_time_retrieved:
                    # check how many days old is the record in the database
                    diff = datetime.datetime.now() - last_time_retrieved[0]
                    if diff.days >= 0 and diff.days < CACHE_TTL:
                        # not old enough - fetch from database
                        print('recently checked - brings from database')
                        cursor.execute(
                            (
                                'select `publication_id` '
                                'from `bare_pub_ids` '
                                'where authors_author_id = %s;'
                            ), (author_id,)
                        )
                        db.commit()

                        pubs = cursor.fetchall()

                        print("There are %d publications.") % len(pubs)

                        cursor.execute(
                            ('select `year`, `citations` '
                             'from `citations_per_year` '
                             'where authors_author_id = %s; '
                            ), (author_id, )
                        )

                        db.commit()

                        citations_per_year = cursor.fetchall()
                        # initialize the dictionary and fill the author's info and
                        # coauthor IDs
                        out = {
                            'name': '',
                            'total_citations': 0,
                            'h_index': 0,
                            'i10_index': 0,
                            'last_time_retrieved': '',
                            'publication_ids': [],
                            'coauthor_ids': [],
                            'citations_per_year': {}
                        }

                        for row in iter(author_data):
                            out['name'] = row[1]
                            out['total_citations'] = row[2]
                            out['h_index'] = row[3]
                            out['i10_index'] = row[4]
                            out['last_time_retrieved'] = row[5]
                            out['coauthor_ids'].append(row[6])

                        for p in iter(pubs):
                            out['publication_ids'].append(p[0])

                        for c in iter(citations_per_year):
                            out['citations_per_year'][c[0]] = c[1]

                        db.close()
                        return jsonify(**out), 200
                    else:
                        print('checked at old times - must refetch from Scholar')
                        cursor.execute(
                            ('delete from `authors` where author_id = %s;'), (author_id,)
                        )
                        db.commit()

                        url = url_for('fetch_author_data', _external=True)
                        data = urllib.urlencode({ 'authorId': author_id })
                        req = urllib2.Request(url, data)

                        try:
                            response = urllib2.urlopen(req, timeout=600)
                        except urllib2.HTTPError as e:
                            db.close()
                            return e.read(), int(e.code)
                        else:
                            db.close()
                            #return redirect('/author/%s' % author_id)
                            return 'waiting for author to be fetched, retry later', 200
                        #return "OK", 200





            '''
            cursor.execute(
                (
                    'select `publication_id` '
                    'from `bare_pub_ids` '
                    'where authors_author_id = %s;'
                ), (author_id,)
            )
            db.commit()

            pubs = cursor.fetchall()

            print("There are %d publications.") % len(pubs)

            cursor.execute(
                ('select `year`, `citations` '
                 'from `citations_per_year` '
                 'where authors_author_id = %s; '
                ), (author_id, )
            )

            db.commit()

            citations_per_year = cursor.fetchall()
            # initialize the dictionary and fill the author's info and
            # coauthor IDs
            out = {
                'name': '',
                'total_citations': 0,
                'h_index': 0,
                'i10_index': 0,
                'last_time_retrieved': '',
                'publication_ids': [],
                'coauthor_ids': [],
                'citations_per_year': {}
            }

            for row in iter(author_data):
                out['name'] = row[1]
                out['total_citations'] = row[2]
                out['h_index'] = row[3]
                out['i10_index'] = row[4]
                out['last_time_retrieved'] = row[5]
                out['coauthor_ids'].append(row[6])

            for p in iter(pubs):
                out['publication_ids'].append(p)

            for c in iter(citations_per_year):
                out['citations_per_year'][c[0]] = c[1]

            db.close()
            return jsonify(**out), 200
            '''
        else:
            # make a POST request to fetch author from google scholar
            url = url_for('fetch_author_data', _external=True)
            data = urllib.urlencode({ 'authorId': author_id })
            req = urllib2.Request(url, data)

            try:
                response = urllib2.urlopen(req, timeout=600)
            except urllib2.HTTPError as e:
                db.close()
                return e.read(), int(e.code)
            else:
                db.close()
                #return redirect('/author/%s' % author_id)
                return 'waiting for author to be fetched, retry later', 200
            '''
            db.close()
            #return redirect('/author/%s' % author_id)
            return 'waiting for author to be fetched, retry later', 200
            '''


@app.route('/publication/<pub_id>', methods=['GET'])
def retrieve_publication(pub_id):
    if not pub_id:
        return "Not found.", 404  # it should never arrive here
    else:
        db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                             user=_db_user, passwd=_db_pass)
        #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

        cursor = db.cursor()
        try:
            cursor.execute("USE scholar_db;")
        except:
            init_db()
            cursor.execute("USE scholar_db;")

        cursor.execute(
            (
                'select `publications`.*, `pub_authors`.author_name, '
                    '`pub_citations_per_year`.year, '
                    '`pub_citations_per_year`.citations '
                'from `publications` '
                'join `pub_authors` on '
                    '`pub_authors`.publications_publication_id = '
                    '`publications`.publication_id '
                'left join `pub_citations_per_year` on '
                    '`pub_citations_per_year`.publications_publication_id = '
                    '`publications`.publication_id '
                'where `publications`.publication_id = %s; '
            ), (pub_id,)
        )

        db.commit()
        pub_data = cursor.fetchall()
        if pub_data:
            # init columns
            out = {
                'publication_id': '',
                'title': '',
                'date': '',
                'total_citations': 0,
                'authors': [],
                'citations_per_year': {},
            }

            for row in iter(pub_data):
                out['publication_id'] = row[0]
                out['title'] = row[1]
                out['date'] = row[2].strftime("%Y-%m-%d")
                out['total_citations'] = row[3]
                au = row[5].decode('utf-8')  # decode utf-8 name
                if not au in out['authors']:
                    out['authors'].append(au)
                out['citations_per_year'][row[6]] = row[7]

            db.close()
            return jsonify(**out), 200

        else:
            # make a POST request to fetch publication data from google scholar
            print('must fetch publication')
            url = url_for('fetch_publication_data', _external=True)
            print('got url for fetch publication')
            data = urllib.urlencode({ 'pub_id': pub_id })
            print('got pub_id for fetch publication')
            req = urllib2.Request(url, data)
            try:
                response = urllib2.urlopen(req, timeout=600)
            except urllib2.HTTPError as e:
                db.close()
                return e.read(), int(e.code)
            else:
                db.close()
                #return redirect('/publication/%s' % pub_id)
                return 'waiting for publication to be fetched, retry later', 200



@app.route('/fetchpublication', methods=['POST'])
def fetch_publication_data():
    """Fetch publication data from Google Scholar and store them in the
    database.
    """
    print('entered fetch publication')
    form = request.form
    try:
        pub_id = form['pub_id']
    except KeyError:
        return "Bad request", 400



    author_id = pub_id.split(':')[0]
    pub_url = ('https://scholar.google.gr/citations?view_op=view_citation&'
               'hl=en&user={0}&citation_for_view={1}').format(author_id,
                                                              pub_id)
    # check if author ID exists in the database
    db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                         user=_db_user, passwd=_db_pass)
    #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

    cursor = db.cursor()
    try:
        cursor.execute("USE scholar_db;")
    except:
        init_db()
        cursor.execute("USE scholar_db;")

    cursor.execute(
        'select * from `authors` where author_id = %s;', (author_id, )
    )

    db.commit()
    row = cursor.fetchone()

    if not row:
        # author does not exist in the database
        # make a POST request to fetch publication data from google scholar
        url = url_for('fetch_author_data', _external=True)
        data = urllib.urlencode({ 'authorId': author_id })
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req, timeout=600)
        except urllib2.HTTPError as e:
            db.close()
            return e.read(), int(e.code)

    print('now entering pubCrawler')

    pubObj = publicationCrawler.create_PublicationObject(pub_url)
    db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                         user=_db_user, passwd=_db_pass)
    #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

    cursor = db.cursor()
    try:
        cursor.execute("USE scholar_db;")
    except:
        init_db()
        cursor.execute("USE scholar_db;")
    try:
        cursor.execute(
            ('insert into publications (publication_id, title, date, '
                'total_citations, authors_author_id) '
             'values (%s, %s, %s, %s, %s); '
            ), (pubObj.pubID, pubObj.title.encode('utf-8'),
                pubObj.publicationDate.strftime("%Y-%m-%d"),
                pubObj.totalCitations, author_id, )
        )

        db.commit()
    except:
        db.rollback()

    for a in iter(pubObj.authors):
        try:
            cursor.execute(
                ('insert into pub_authors (author_name, '
                    'publications_publication_id) '
                 'values (%s, %s);'
                ), (a.encode('utf-8'), pubObj.pubID, )
            )
            db.commit()
        except:
            db.rollback()

    for c in iter(pubObj.citationGraph):
        try:
            cursor.execute(
                ('insert into pub_citations_per_year (year, citations, '
                    'publications_publication_id) '
                 'values (%s, %s, %s);'
                ), (c[0], c[1], pubObj.pubID, )
            )
            db.commit()
        except:
            db.rollback()

    db.close()

    '''
    q_pub = taskqueue.Queue('PublicationsQueue')
    task = taskqueue.Task(url='/crawlPublication', params={'pub_id': pub_id})
    q_pub.add(task)
    '''
    return "OK", 200


'''
@app.route('/crawlPublication', methods=['POST'])
def crawl_publication():
    form = request.form
    try:
        pub_id = form['pub_id']
    except KeyError:
        return "Bad request", 400
    #author_obj = authorCrawler.authorCrawler(author, 3)
    author_id = pub_id.split(':')[0]
    pub_url = ('https://scholar.google.gr/citations?view_op=view_citation&'
               'hl=en&user={0}&citation_for_view={1}').format(author_id,
                                                              pub_id)


    pubObj = publicationCrawler.create_PublicationObject(pub_url)
    db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                         user=_db_user, passwd=_db_pass)
    #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

    cursor = db.cursor()
    try:
        cursor.execute("USE scholar_db;")
    except:
        init_db()
        cursor.execute("USE scholar_db;")
    try:
        cursor.execute(
            ('insert into publications (publication_id, title, date, '
                'total_citations, authors_author_id) '
             'values (%s, %s, %s, %s, %s); '
            ), (pubObj.pubID, pubObj.title,
                pubObj.publicationDate.strftime("%Y-%m-%d"),
                pubObj.totalCitations, author_id, )
        )

        db.commit()
    except:
        db.rollback()

    for a in iter(pubObj.authors):
        try:
            cursor.execute(
                ('insert into pub_authors (author_name, '
                    'publications_publication_id) '
                 'values (%s, %s);'
                ), (a.encode('utf-8'), pubObj.pubID, )
            )
            db.commit()
        except:
            db.rollback()

    for c in iter(pubObj.citationGraph):
        try:
            cursor.execute(
                ('insert into pub_citations_per_year (year, citations, '
                    'publications_publication_id) '
                 'values (%s, %s, %s);'
                ), (c[0], c[1], pubObj.pubID, )
            )
            db.commit()
        except:
            db.rollback()

    db.close()
'''




def init_db():
    """Initialize database schema."""
    db = MySQLdb.connect(host=_db_host, unix_socket=_db_unix_socket,
                         user=_db_user, passwd=_db_pass)
    #db = MySQLdb.connect("localhost","root","gu1t@rri5ta")

    cursor = db.cursor()

    cursor.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
    cursor.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, "
                   "FOREIGN_KEY_CHECKS=0;")
    cursor.execute("SET @OLD_SQL_MODE=@@SQL_MODE, "
                   "SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS scholar_db ;")
    db.commit()

    cursor.execute("USE scholar_db ;")
    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.authors ( \
                   author_id VARCHAR(45) COLLATE utf8_unicode_ci NOT NULL, \
                   name VARCHAR(45) COLLATE utf8_unicode_ci NULL, \
                   total_citations INT NULL, \
                   h_index INT NULL, \
                   i10_index INT NULL, \
                   last_time_retrieved DATETIME NULL, \
                   PRIMARY KEY (author_id), \
                   UNIQUE INDEX author_id_UNIQUE (author_id ASC)) \
                   ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.coauthors ( \
                   coauthor_id VARCHAR(45) COLLATE utf8_unicode_ci NULL, \
                   authors_author_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL, \
                   PRIMARY KEY (coauthor_id, authors_author_id), \
                   CONSTRAINT fk_coauthors_authors1 \
                   FOREIGN KEY (authors_author_id) \
                   REFERENCES scholar_db.authors (author_id) \
                   ON DELETE CASCADE \
                   ON UPDATE CASCADE) \
                   ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.citations_per_year "
                   "( \
                   year INT NOT NULL, \
                   citations INT NULL, \
                    authors_author_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL,\
                    PRIMARY KEY (year, authors_author_id), \
                    INDEX fk_citations_per_year_authors1_idx "
                        "(authors_author_id ASC), \
                    CONSTRAINT fk_citations_per_year_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE CASCADE \
                    ON UPDATE CASCADE) \
                    ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.publications ( \
                    publication_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL, \
                    title TEXT COLLATE utf8_unicode_ci NULL, \
                    date DATE NULL, \
                    total_citations INT NULL, \
                    authors_author_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL, \
                    PRIMARY KEY (publication_id), \
                    INDEX fk_publications_authors1_idx "
                        "(authors_author_id ASC), \
                    CONSTRAINT fk_publications_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE CASCADE \
                    ON UPDATE CASCADE) \
                    ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.pub_authors ( \
                   author_name VARCHAR(45) COLLATE utf8_unicode_ci NULL, \
                   publications_publication_id VARCHAR(45) COLLATE "
                        "utf8_unicode_ci NOT NULL, \
                   PRIMARY KEY (author_name, publications_publication_id), \
                   INDEX fk_pub_authors_publications1_idx "
                        "(publications_publication_id ASC), \
                   CONSTRAINT fk_pub_authors_publications1 \
                   FOREIGN KEY (publications_publication_id) \
                   REFERENCES scholar_db.publications (publication_id) \
                   ON DELETE CASCADE \
                   ON UPDATE CASCADE) \
                   ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS "
                        "scholar_db.pub_citations_per_year ( \
                    year INT NOT NULL, \
                    citations INT NULL, \
                    publications_publication_id VARCHAR(45) COLLATE "
                        "utf8_unicode_ci NOT NULL, \
                    PRIMARY KEY (year, publications_publication_id), \
                    INDEX fk_pub_citations_per_year_publications1_idx "
                        "(publications_publication_id ASC), \
                    CONSTRAINT fk_pub_citations_per_year_publications1 \
                    FOREIGN KEY (publications_publication_id) \
                    REFERENCES scholar_db.publications (publication_id) \
                    ON DELETE CASCADE \
                    ON UPDATE CASCADE) \
                    ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("CREATE TABLE IF NOT EXISTS scholar_db.bare_pub_ids( \
                    publication_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL, \
                    authors_author_id VARCHAR(45) COLLATE utf8_unicode_ci "
                        "NOT NULL, \
                    PRIMARY KEY (publication_id), \
                    CONSTRAINT fk_bare_pub_ids_authors1 \
                    FOREIGN KEY (authors_author_id) \
                    REFERENCES scholar_db.authors (author_id) \
                    ON DELETE CASCADE \
                    ON UPDATE CASCADE) \
                    ENGINE = InnoDB "
                   "DEFAULT CHARSET=utf8;")

    cursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
    cursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")

    db.commit()

    db.close()