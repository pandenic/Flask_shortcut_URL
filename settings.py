"""Contains general settings for YaCut app."""
import os
from dataclasses import dataclass

INDEX_PAGE = 'index.html'
API_URL = '/api/'

ORIGINAL_URL_MAX_LENGTH = 256
SHORT_URL_MAX_LENGTH = 16
SHORT_URL_DEFAULT_LENGTH = 6
SHORT_URL_REGEX_PATTERN = r'^[A-Za-z0-9]{0,16}$'


@dataclass
class HTTPMethods:
    """Describes HTTP methods names."""

    GET: str = 'GET'
    POST: str = 'POST'


class Config(object):
    """Describes configs for a flask_yacut project."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
