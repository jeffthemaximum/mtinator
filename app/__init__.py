from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import flask

from .set_flask_config import set_flask_config

def create_app():
    app = flask.Flask(__name__)

    set_flask_config(app)

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    return {
        'app': app,
        'db': db,
        'migrate': migrate
    }
