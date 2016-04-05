class Config(object):

  DEBUG = True
  CSRF_ENABLED = False

  SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://programize2:scholar123!@173.194.242.182/citation_analysis_db?unix_socket=/cloudsql/citation-analysis:sql'
  #SQLALCHEMY_DATABASE_URI = 'mysql://root:scrooge@localhost/citation_analysis_db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_POOL_SIZE = 12
  SQLALCHEMY_MAX_OVERFLOW = 0
  #SQLALCHEMY_ECHO = True

  BASIC_AUTH_USERNAME = 'me'
  BASIC_AUTH_PASSWORD = 'andmypassword'
