import os

class Config(object):
    SECRET_KEY=os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopingConfig(Config):
    DEBUG=True
    # SQLALCHEMY_ECHO = True
    ENV = 'local'

class TestingConfig(Config):
    DEBUG=True
    TESTING=True
    WTF_CSRF_ENABLED = False
    ENV = 'testing'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:productionpass@localhost/mini_blog'
    ENV = 'production'
    