"""Contains API view funstions for the YaCut app."""
import re
from http import HTTPStatus
from typing import Tuple

from flask import Response, jsonify, request, url_for
from settings import (API_URL, SHORT_URL_DEFAULT_LENGTH,
                      SHORT_URL_REGEX_PATTERN, HTTPMethods)

from yacut import app, db
from yacut.error_handlers import ErrorMessages, InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.views import index_view


@app.route(f'{API_URL}id/', methods=[HTTPMethods.POST])
def create_short_url() -> Tuple[Response, HTTPStatus]:
    """Create short URL from original URL and add to database."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            ErrorMessages.EMPTY_REQUEST_BODY, HTTPStatus.BAD_REQUEST,
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            ErrorMessages.ORIGINAL_URL_NOT_IN_REQUEST, HTTPStatus.BAD_REQUEST,
        )
    if (
        'custom_id' in data
        and data['custom_id']
        and re.search(SHORT_URL_REGEX_PATTERN, data['custom_id'])
        and URLMap.query.filter_by(short=data['custom_id']).first()
    ):
        raise InvalidAPIUsage(
            ErrorMessages.SHORT_URL_EXISTS, HTTPStatus.BAD_REQUEST,
        )
    if (
        'custom_id' in data
        and data['custom_id']
        and not re.search(SHORT_URL_REGEX_PATTERN, data['custom_id'])
    ):
        raise InvalidAPIUsage(
            ErrorMessages.SHORT_URL_WRONG_FORMAT, HTTPStatus.BAD_REQUEST,
        )
    if (
        'custom_id' in data
        and not data['custom_id']
        or 'custom_id' not in data
    ):
        data['custom_id'] = get_unique_short_id(SHORT_URL_DEFAULT_LENGTH)
    url_map = URLMap()
    url_map.from_dict(
        {
            'original': data['url'],
            'short': data['custom_id'],
        },
    )
    db.session.add(url_map)
    db.session.commit()

    url_map_dict = url_map.to_dict()
    return (
        jsonify(
            {
                'url': url_map_dict['original'],
                'short_link': f'{url_for(index_view.__name__, _external=True)}{url_map_dict["short"]}',
            },
        ),
        HTTPStatus.CREATED,
    )


@app.route(f'{API_URL}id/<string:short_id>/', methods=[HTTPMethods.GET])
def get_original_url(short_id: str) -> Tuple[Response, HTTPStatus]:
    """Return original URL from short URL."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(
            ErrorMessages.SHORT_URL_NOT_IN_DB, HTTPStatus.NOT_FOUND,
        )
    url_map_dict = url_map.to_dict()
    return (
        jsonify(
            {
                'url': url_map_dict['original'],
            },
        ),
        HTTPStatus.OK,
    )
