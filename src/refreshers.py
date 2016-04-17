from datetime import datetime
from google.appengine.api import taskqueue
from main import app, db
from models import Author
from models import Publication
from sqlalchemy import or_, func
from sqlalchemy.orm import load_only

P = 0.05

@app.route('/author/refresh', methods=['GET'])
def refresh_authors():
  """
  Schedules some of the out-dated authors to be refreshed.
  """

  OUT_DATE_LIMIT = 30
  FETCH_LIMIT = 10000

  authors = Author.query.filter(Author.scholar_id != None, func.rand() < P, or_(Author.retrieved_at == None, func.now() > func.adddate(Author.retrieved_at, OUT_DATE_LIMIT))).options(load_only('scholar_id')).limit(FETCH_LIMIT).all()
  count = 0
  for author in authors:
      queue = taskqueue.Queue('author-fetchers')
      task = taskqueue.Task(url='/author/crawl', params={'scholar_id': author.scholar_id})
      queue.add(task)
      count += 1

  print 'Had ' + str(count) + ' authors refreshed.'
  return 'Refreshed.'

@app.route('/publication/refresh', methods=['GET'])
def refresh_publications():
  """
  Schedules some of the out-dated publications to be refreshed.
  """

  OUT_DATE_LIMIT = 180
  FETCH_LIMIT = 1000

  publications = Publication.query.filter(Publication.scholar_id != None, func.rand() < P, or_(Publication.retrieved_at == None, func.now() > func.adddate(Publication.retrieved_at, OUT_DATE_LIMIT))).options(load_only('scholar_id')).limit(FETCH_LIMIT).all()
  count = 0
  for publication in publications:
      queue = taskqueue.Queue('publication-fetchers')
      task = taskqueue.Task(url='/publication/crawl', params={'scholar_id': publication.scholar_id})
      queue.add(task)
      count += 1

  print 'Had ' + str(count) + ' publications refreshed.'
  return 'Refreshed.'