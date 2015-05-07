try:
    from secret import CSRF_SECRET_KEY, SESSION_KEY
except:
    # let's provide a default, for now !!!
    CSRF_SECRET_KEY = "some secret"
    SESSION_KEY = "or other"

class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = CSRF_SECRET_KEY
    CSRF_SESSION_KEY = SESSION_KEY

class Production(Config):
    DEBUG = False
    CSRF_ENABLED = True

class Development(Config):
    DEBUG = True
    CSRF_ENABLED = False
