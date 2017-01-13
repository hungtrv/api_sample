import logging

from flask import Flask
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from main.config import config

app = Flask(__name__)
app.config.from_object(config)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

#api = Blueprint('api', __name__)

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()

CORS(app)


def _register_subpackages():
    from main.models import *
    from main.errors import *
    from main.auth import *
    from main.controllers.v1 import *

_register_subpackages()

# Register blue print at last when all the code for blue print is imported
from main.controllers.v1 import api
app.register_blueprint(api, url_prefix='/v1')
