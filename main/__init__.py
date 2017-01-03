import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from main.config import config

app = Flask(__name__)
app.config.from_object(config)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

CORS(app)

def _register_subpackages():
    from main.models import *
    from main.controllers import *
    from main.errors import *

_register_subpackages()
