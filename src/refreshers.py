from datetime import datetime
from main import app, db
from models import Author
from models import Publication
import random
from sqlalchemy import or_, func
from google.appengine.api import taskqueue

p = 0.05

@app.route('/author/refresh', methods=['GET'])
def refresh_authors():
  """
  Schedules some of the out-dated authors to be refreshed.
  """

  authors = Author.query.filter(Author.scholar_id != None, or_(Author.retrieved_at == None, func.now() > func.adddate(Author.retrieved_at, 30))).all()
  count = 0
  for author in authors:
    if random.random() < p:
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

  publications = Publication.query.filter(Publication.scholar_id != None, or_(Publication.retrieved_at == None, func.now() > func.adddate(Publication.retrieved_at, 180))).all()
  count = 0
  for publication in publications:
    if random.random() < p:
        queue = taskqueue.Queue('publication-fetchers')
        task = taskqueue.Task(url='/publication/crawl', params={'scholar_id': publication.scholar_id})
        queue.add(task)
        count += 1

  print 'Had ' + str(count) + ' publications refreshed.'
  return 'Refreshed.'