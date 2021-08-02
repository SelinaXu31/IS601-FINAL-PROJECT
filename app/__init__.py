from flask import Flask


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    assets = Environment()  # Create an assets environment
    assets.init_app(app)

    with app.app_context():
        from .profile import profile
        from .home import home
        from .products import products
        from .assets import compile_static_assets

        app.register_blueprint(profile.account_bp)
        app.register_blueprint(home.home_bp)
        app.register_blueprint(products.product_bp)

        compile_static_assets(assets)

        return app
