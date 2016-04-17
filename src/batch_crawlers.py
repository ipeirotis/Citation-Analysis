from flask import url_for
from main import app
from models import Author
from models import Publication
from sqlalchemy import or_, func
from sqlalchemy.orm import load_only
import time
from urllib import urlencode
from urllib2 import Request, urlopen

@app.route('/author/batch-crawl', methods=['GET'])
def batch_crawl_authors():
  """
  Crawls Google Scholar in order to retrieve information about authors in
  batches.
  """

  FETCH_LIMIT = 1000
  SLEEP_TIME = 2

  while True:

    authors = Author.query.filter(Author.scholar_id != None, Author.retrieved_at == None).options(load_only('scholar_id')).order_by(func.rand()).limit(FETCH_LIMIT).all()

    count = 0
    for author in authors:
        url = url_for('crawl_author', _external=True)
        data = urlencode({'scholar_id': author.scholar_id})
        req = Request(url, data)
        res = urlopen(req, timeout=30)
        count += 1
        time.sleep(SLEEP_TIME)

    print 'Crawled ' + str(count) + ' authors.'
    if count == 0:
      break

  return 'Done.'

@app.route('/publication/batch-crawl', methods=['GET'])
def batch_crawl_publications():
  """
  Crawls Google Scholar in order to retrieve information about publications
  in batches.
  """

  FETCH_LIMIT = 1000
  SLEEP_TIME = 10

  while True:

    publications = Publication.query.filter(Publication.scholar_id != None, Publication.retrieved_at == None).options(load_only('scholar_id')).order_by(func.rand()).limit(FETCH_LIMIT).all()

    count = 0
    for publication in publications:
        url = url_for('crawl_publication', _external=True)
        data = urlencode({'scholar_id': publication.scholar_id})
        req = Request(url, data)
        res = urlopen(req, timeout=30)
        count += 1
        time.sleep(SLEEP_TIME)

    print 'Crawled ' + str(count) + ' publications.'
    if count == 0:
      break

  return 'Done.'
