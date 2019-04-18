#!/usr/bin/env python3

# This is the entrypoint to pastebing

from flask_core.app import create_app
from flask_core.config import Config

from . import models

# If you add more blueprints, add them here
from .main import bp as main_bp

config = Config()
app = create_app(config)

app.register_blueprint(main_bp)
