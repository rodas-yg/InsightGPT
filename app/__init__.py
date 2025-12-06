import os
from flask import Flask
from .extensions import init_extensions
from .routes import main as main_bp
from config import Config

# Factory that creates and configures the Flask application.
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object(Config)

    # Ensure instance and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions (if any in future)
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
