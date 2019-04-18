#!/usr/bin/env python3

# This is the entrypoint to bing_drive

from flask_core.app import create_app
from flask_core.config import Config
from flask_swagger_ui import get_swaggerui_blueprint

from . import models

# If you add more blueprints, add them here
from .main import bp as main_bp

config = Config()
app = create_app(config)

# Swagger BS
swaggerui_blueprint = get_swaggerui_blueprint(
    "/staff/secret/1gbdfte/swagger",  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    "/docs/swag.json",
    config={"app_name": "Prism Api"},
)

app.register_blueprint(swaggerui_blueprint, url_prefix="/staff/secret/1gbdfte/swagger")

app.register_blueprint(main_bp)
