# Initialize and configure the application.

import config
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_object(config.Config)

# Connect to the database.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Set up authentication and authorization.

from flask.ext.login import LoginManager, login_required
from models import User

login_manager = LoginManager(app)

@login_manager.request_loader
def do_auth(request):
  auth = request.authorization
  if auth:
    user = User.get()
    if auth.username == user.id and auth.password == user.password:
      return user
  return None

#@login_required
def auth(**kw):
  pass

from flask.ext.restless import APIManager, ProcessingException

apimanager = APIManager(app, flask_sqlalchemy_db = db)

# Set up the organizations API.

from models import Organization
import math

apimanager.create_api(Organization, methods=['DELETE', 'GET', 'POST', 'PUT'],
                      include_methods = ['children_ids', 'ancestor_ids',
                                         'descendant_ids', 'ancestor_tree'],
                      exclude_columns = ['authors'],
                      preprocessors = {'DELETE_SINGLE': [auth],
                                       'DELETE_MANY':  [auth],
                                       'POST': [auth],
                                       'PUT_SINGLE': [auth],
                                       'PUT_MANY': [auth]},
                      results_per_page = None)

@app.route('/api/organization/root', methods=['GET'])
def get_root_organizations():
  """
  Gets all root organizations.
  """

  page = int(request.args.get('page'))
  per_page = int(request.args.get('per_page'))

  query = Organization.query.filter_by(parent_id = None).order_by('id').paginate(page, per_page, False)
  total = query.total
  organizations = query.items
  roots = []
  for organization in organizations:
    roots.append({'id': organization.id, 'name': organization.name, 'location': organization.location, 'website_url': organization.website_url})
  result = {'roots': roots, 'total': total, 'total_pages': int(math.ceil(total / float(per_page)))}
  return jsonify(**result)

@app.route('/api/organization/<id>/tree', methods=['GET'])
def get_organization_tree(id):
  """
  Gets the hierarchical tree that has an organization as the root.
  """

  organization = Organization.query.filter_by(id = id).first()
  result = {'tree': organization.descendant_tree()}
  return jsonify(**result)

# Set up the authors API.

from models import Author
from google.appengine.api import taskqueue
from datetime import datetime

def prea(search_params = None, **kw):
  if search_params is None:
    return
  if 'filters' not in search_params:
    return
  filters = search_params['filters']
  if len(filters) != 1:
    return
  filter = filters[0]
  if 'name' not in filter:
    return
  if filter['name'] != 'scholar_id':
    return
  if filter['op'] != '==':
    return
  scholar_id = filter['val']
  author = Author.query.filter_by(scholar_id = scholar_id).first()
  if (author is None or author.retrieved_at is None):
    queue = taskqueue.Queue('author-fetchers')
    task = taskqueue.Task(url='/author/crawl', params={'scholar_id': scholar_id})
    queue.add(task)
    raise ProcessingException(description = 'Try later.', code = 202)
  elif (datetime.now() - author.retrieved_at).days > 60:
    queue = taskqueue.Queue('author-fetchers')
    task = taskqueue.Task(url='/author/crawl', params={'scholar_id': scholar_id})
    queue.add(task)

apimanager.create_api(Author, methods=['DELETE', 'GET', 'POST', 'PUT'],
                      include_methods = ['organization_ids', 'organization_tree'],
                      exclude_columns = [],
                      preprocessors = {'DELETE_SINGLE': [auth],
                                       'DELETE_MANY':  [auth],
                                       'POST': [auth],
                                       'PUT_SINGLE': [auth],
                                       'PUT_MANY': [auth],
                                       'GET_MANY': [prea]},
                      results_per_page = None)

# Set up the publications API.

from models import Publication

def prep(search_params = None, **kw):
  if search_params is None:
    return
  if 'filters' not in search_params:
    return
  filters = search_params['filters']
  if len(filters) != 1:
    return
  filter = filters[0]
  if 'name' not in filter:
    return
  if filter['name'] != 'scholar_id':
    return
  if filter['op'] != '==':
    return
  scholar_id = filter['val']
  publication = Publication.query.filter_by(scholar_id = scholar_id).first()
  if (publication is None or publication.retrieved_at is None):
    queue = taskqueue.Queue('publication-fetchers')
    task = taskqueue.Task(url='/publication/crawl', params={'scholar_id': scholar_id})
    queue.add(task)
    raise ProcessingException(description = 'Try later.', code = 202)
  elif (datetime.now() - publication.retrieved_at).days > 365:
    queue = taskqueue.Queue('publication-fetchers')
    task = taskqueue.Task(url='/publication/crawl', params={'scholar_id': scholar_id})
    queue.add(task)

apimanager.create_api(Publication, methods=['GET'],
                      include_methods = [],
                      exclude_columns = [],
                      preprocessors = {'GET_MANY': [prep]},
                      results_per_page = None)

@app.route('/')
def welcome():
  """
  Welcomes.
  """
  message = "This is the data management component of the citation analysis project."
  return message

import crawlers

import refreshers

if __name__ == '__main__':
  app.run(debug = app.config['DEBUG'])
