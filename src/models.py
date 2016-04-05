from main import db

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

coauthors = db.Table('coauthor',
                     db.Column('author_id', db.Integer,
                               db.ForeignKey('author.id')),
                     db.Column('coauthor_id', db.Integer,
                               db.ForeignKey('author.id'))
)

author_publications = db.Table('author_publication',
                               db.Column('author_id', db.Integer,
                                         db.ForeignKey('author.id')),
                               db.Column('publication_id', db.Integer,
                                         db.ForeignKey('publication.id'))
)

class Author(db.Model):
  """
  A class that represents authors.
  """

  __tablename__ = 'author'
  """
  The name of the table where authors are stored.
  """

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  """
  The ID of the author.
  """

  name = db.Column(db.String(256), nullable = False)
  """
  The name of the author.
  """

  title = db.Column(db.String(256), nullable = True)
  """
  The title (e.g. associate professor) of the author.
  """

  organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = True)
  """
  The ID of the organization where the author belongs.
  """

  organization = db.relation('Organization', foreign_keys=[organization_id], backref = "authors")
  """
  The organization where the author belongs.
  """

  year_of_phd = db.Column(db.Integer, nullable = True)
  """
  The year when the author received his/her Ph.D.
  """

  tenured = db.Column(db.Boolean, nullable = True)
  """
  Whether the author is tenured.
  """

  scholar_id = db.Column(db.String(64), nullable = True, unique = True)
  """
  The ID of the author in Google Scholar.
  """

  website_url = db.Column(db.String(256), nullable = True)
  """
  The URL of the website of the author.
  """

  email_domain = db.Column(db.String(256), nullable = True)
  """
  The domain of the email of the author.
  """

  total_citations = db.Column(db.Integer, nullable = True)
  """
  The total citations for the author.
  """

  h_index = db.Column(db.Numeric(precision  = 10, scale = 2), nullable = True)
  """
  The value of the h-index metric for the author.
  """

  i10_index = db.Column(db.Numeric(precision  = 10, scale = 2), nullable = True)
  """
  The value of the i10-index metric for the author.
  """

  retrieved_at = db.Column(db.DateTime, nullable = True)
  """
  The date and time when information about the author was last retrieved 
  from Google Scholar.
  """

  coauthors = db.relationship("Author", secondary = coauthors,
                              primaryjoin = id == coauthors.c.author_id,
                              secondaryjoin = id == coauthors.c.coauthor_id)
  """
  The co-authors of the author.
  """

  publications = db.relationship("Publication",
                              secondary = author_publications,
                              backref = "authors")
  """
  The publications of the author.
  """

  citations_per_year = db.relationship("AuthorCitationsPerYear",
                              cascade="all, delete-orphan")
  """
  The citations per year for the author.
  """

  def organization_tree(self):
    """
    Gets the names of the organization, where the author belongs, and all
    its ancestors (starting from the root of the family tree) separated with
    ' :: '.
    """
    if not self.organization:
      return ''
    organizations = [ self.organization ]
    organizations.extend(self.organization.ancestors())
    return ' :: '.join([ a.name for a in reversed(organizations) ])

  def organization_ids(self):
    """
    Gets the ID's of the organization, where the author belongs, and all
    its ancestors (starting from the root of the family tree).
    """
    if not self.organization:
      return []
    organizations = [ self.organization ]
    organizations.extend(self.organization.ancestors())
    return [ a.id for a in reversed(organizations) ]

class AuthorCitationsPerYear(db.Model):
  """
  A class that represents the citations for authors per year.
  """

  __tablename__ = 'author_citations_per_year'
  """
  The name of the table where citations per year are stored.
  """

  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key = True)
  """
  The ID of the author.
  """

  author = db.relation('Author')
  """
  The author.
  """

  year = db.Column(db.Integer, primary_key = True)
  """
  The year.
  """

  citations = db.Column(db.Integer, nullable = False)
  """
  The citations for the author in the year.
  """

class Organization(db.Model):
  """
  A class that represents organizations (e.g. universities, schools,
  departments).
  """

  __tablename__ = 'organization'
  """
  The name of the table where organizations are stored.
  """

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  """
  The ID of the organization.
  """

  name = db.Column(db.String(256), nullable = False)
  """
  The name of the organization.
  """

  parent_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = True)
  """
  The ID of the parent organization.
  """

  parent = db.relation('Organization', remote_side = [id], backref = "children")
  """
  The parent organization.
  """

  location = db.Column(db.String(256), nullable = True)
  """
  The location of the organization.
  """

  website_url = db.Column(db.String(256), nullable = True)
  """
  The URL of the website of the organization.
  """

  children_source_url = db.Column(db.String(256), nullable = True)
  """
  The URL where the children of the organization can be retrieved from.
  """

  def children_ids(self):
    """
    Gets the ID's of the children of the organization.
    """
    return [ c.id for c in self.children ]

  def ancestors(self):
    """
    Gets the ancestors of the organization (starting from its parent and
    ending at the root of the family tree).
    """
    if self.parent is None:
      return []
    l = [ self.parent ]
    l.extend(self.parent.ancestors())
    return l

  def ancestor_ids(self):
    """
    Gets the ID's of the ancestors of the organization (starting from its
    parent and ending at the root of the family tree).
    """
    return [ a.id for a in self.ancestors() ]

  def ancestor_tree(self):
    """
    Gets the names of the ancestors of the organization (starting from the
    root of the family tree) separated with ' :: '.
    """
    ancestors = self.ancestors()
    if not ancestors:
      return None
    return ' :: '.join([ a.name for a in reversed(ancestors) ])

  def descendants(self):
    """
    Gets the descendants of the organization (starting from its children and
    ending at the leaves of the family tree).
    """
    if not self.children:
      return []
    l = []
    for c in self.children:
      l.append(c)
      l.extend(c.descendants())
    return l

  def descendant_tree(self):
    """
    Gets the descendants of the organization as a tree (starting from the
    children).
    """
    descendants = []
    for c in self.children:
      descendants.append({ 'id': c.id, 'name': c.name, 'children': c.descendant_tree(), 'number_of_authors': c.number_of_authors() })
    return descendants

  def descendant_ids(self):
    """
    Gets the ID's of the descendants of the organization (starting from its children and
    ending at the leaves of the family tree).
    """
    return [ d.id for d in self.descendants() ]

  def number_of_authors(self):
    """
    Gets the number of the authors that belong to the organization.
    """
    return len(self.authors);

class Publication(db.Model):
  """
  A class that represents publications.
  """

  __tablename__ = 'publication'
  """
  The name of the table where publications are stored.
  """

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  """
  The ID of the publication.
  """

  type = db.Column(db.String(16), nullable = True)
  """
  The type of the publication.
  """

  title = db.Column(db.String(512), nullable = True)
  """
  The title of the publication.
  """

  author_names = db.Column('authors', db.String(512), nullable = True)
  """
  The names of the authors of the publication separated with commas.
  """

  scholar_id = db.Column(db.String(64), nullable = True, unique = True)
  """
  The ID of the publication in Google Scholar.
  """

  year_of_publication = db.Column(db.Integer, nullable = True)
  """
  The year when the publication was published.
  """

  total_citations = db.Column(db.Integer, nullable = True)
  """
  The total citations for the publication.
  """

  retrieved_at = db.Column(db.DateTime, nullable = True)
  """
  The date and time when information about the publication was last retrieved
  from Google Scholar.
  """

  citations_per_year = db.relationship("PublicationCitationsPerYear",
                              cascade="all, delete-orphan")
  """
  The citations per year for the publication.
  """

class PublicationCitationsPerYear(db.Model):
  """
  A class that represents the citations for publications per year.
  """

  __tablename__ = 'publication_citations_per_year'
  """
  The name of the table where citations per year are stored.
  """

  publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key = True)
  """
  The ID of the publication.
  """

  publication = db.relation('Publication')
  """
  The publication.
  """

  year = db.Column(db.Integer, primary_key = True)
  """
  The year.
  """

  citations = db.Column(db.Integer, nullable = False)
  """
  The citations for the publication in the year.
  """

from main import app
from flask.ext.login import UserMixin
class User(UserMixin):
  """
  A class that represents application users.
  """

  def __init__(self, username, password):
    """
    Constructs a user with the given username and password.
    """
    self.id = username
    self.password = password

  @classmethod
  def get(cls):
    """
    Gets the only valid application user.
    """
    return User(app.config['BASIC_AUTH_USERNAME'], app.config['BASIC_AUTH_PASSWORD'])