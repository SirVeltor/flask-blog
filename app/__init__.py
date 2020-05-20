from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging import StreamHandler
import logging


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)


    if app.config.get('TESTING'):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py')
    
    configure_logging(app)    


    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de los blueprints
    from .public import public_bp
    app.register_blueprint(public_bp)
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    register_error_handlers(app)

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
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )