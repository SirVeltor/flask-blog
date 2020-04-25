from os.path import abspath, dirname
import os

# Definimos el directorio de la aplicación

BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS = False


# Entornos de la aplicación

APP_ENV_LOCAL = 'local'
APP_ENV_TEST = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_PRODUCTION = 'production'
ENV = ''