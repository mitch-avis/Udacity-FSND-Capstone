import logging
from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

from capstone_app.config.auth_config import auth_config
from capstone_app.config.env_config import Config
from capstone_app.config.logger_config import LOGGING_CONFIG
from capstone_app.database.models import setup_db

# Logger formatting
dictConfig(LOGGING_CONFIG)
# Create logger
log = logging.getLogger(__name__)


def create_app(config_class=Config):
    """Creates the Flask application."""
    # Create Flask app
    app = Flask(__name__)
    # Load flask config
    app.config.from_object(config_class)
    # Load auth config secrets
    app.secret_key = auth_config["WEBAPP"]["SECRET_KEY"]
    # Configure CORS
    allowed_origins = config_class.ALLOWED_ORIGINS
    CORS(app, origins=allowed_origins)
    # Finish app initialization
    with app.app_context():
        # Initialize database
        _initialize_database(app, config_class)
        # Add Flask Blueprints to app
        _add_blueprints(app)
        # Return initialized app
        return app


def _initialize_database(app: Flask, config_class: Config):
    """Initializes the database using loaded configuration variables."""
    # Load database variables from config class
    db_user = config_class.DB_USER
    db_password = config_class.DB_PASSWORD
    db_host = config_class.DB_HOST
    db_port = config_class.DB_PORT
    db_name = config_class.DB_NAME
    # Construct database path from variables
    db_path = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    # Initialize database
    setup_db(app, db_path)


def _add_blueprints(app: Flask):
    """Registers Flask Blueprints."""
    # pylint: disable=C0415
    from capstone_app.api.views import api_bp
    from capstone_app.auth.views import auth_bp
    from capstone_app.errors.views import errors_bp

    # Add error handlers blueprint to app
    app.register_blueprint(errors_bp)
    # Add OAuth blueprint to app
    app.register_blueprint(auth_bp, url_prefix="/")
    # Add API endpoints blueprint to app
    app.register_blueprint(api_bp, url_prefix="/")
