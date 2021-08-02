from flask import Flask
from flask_assets import Environment
from .assets import compile_assets
from flask_sqlalchemy import SQLAlchemy

assets = Environment()
db = SQLAlchemy()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        return app


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_assets

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

        if app.config['FLASK_ENV'] == 'development':
            compile_assets(app)

        return app
