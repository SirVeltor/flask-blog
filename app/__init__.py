from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from .common.filters import format_datetime


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)


    if app.config.get('TESTING'):
        app.config.from_pyfile('config_testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py')



    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db)

    #Registro de los filtros
    register_filters(app)

    # Registro de los blueprints
    from .public import public_bp
    app.register_blueprint(public_bp)
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    register_error_handlers(app)

    configure_logging(app)

    return app

def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_tempalte("500.html"), 500

    @app.errorhandler(404)
    def error_400_handler(e):
        print('llamando al error handler 400')
        return render_template("404.html"), 404

def configure_logging(app):

    # Eliminamos los posibles manejadores del logger por defecto (si existen)
    del app.logger.handlers[:]

    #Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []

    #Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s'))
    handlers.append(console_handler)

    file_handler = logging.FileHandler("flask-blog.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s'))
    handlers.append(file_handler)

    #Añadimos cada uno de los handlers a cada uno de los loggers

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime