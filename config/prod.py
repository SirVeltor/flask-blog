from .default import *
import os

SECRET_KEY = os.urandom(24)

ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'mysql://root:veltor7550436@localhost/mini_blog'