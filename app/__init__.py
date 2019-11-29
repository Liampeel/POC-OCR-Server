from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

# TODO: #11 Add database functionality to web app
# db = ...
bootstrap = Bootstrap()


def create_app(config_class=Config):
    """Creates the Flask app.

    :param config_class: Config class to use, default is the base config
        stored in the repository.
    """
    # Initiate Flask app and config
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initiate app components
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Initialise the app components we do not want when testing
    if not app.debug and not app.testing:
        # TODO: #16 Implement logging in the web app
        pass  # Nothing to set up at the moment so pass

    return app


from app import models
