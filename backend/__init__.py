__version__ = "0.1.0"

import random
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, send_from_directory

import backend.constants as constants
from backend.endpoints import frontend_handler
from backend.endpoints import document_handler
from backend.config import config
from backend.database import db, migrate

sentry_sdk.init(
    dsn="https://66b8f95c554065bbc3bd32ccef913208@o561713.ingest.us.sentry.io/4507502201995264",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    enable_tracing=True,
    integrations = [
        FlaskIntegration(
            transaction_style="url",
        ),
    ],
)


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)

    return app

app = create_app(constants.General.config_mode)

app.register_blueprint(frontend_handler.bp)
app.register_blueprint(document_handler.bp)

asgi_app = WsgiToAsgi(app)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))