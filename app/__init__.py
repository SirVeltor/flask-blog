from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module):
    print('settings module en create_app -->', settings_module)
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

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

    return app


