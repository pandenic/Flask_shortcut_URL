"""Contains error handlers for the YaCut app."""
from dataclasses import dataclass
from http import HTTPStatus
from typing import Tuple

from flask import Response, jsonify, render_template

from yacut import app, db
from yacut.settings import SHORT_URL_MAX_LENGTH


@dataclass
class ErrorMessages:
    """Contains error messages."""

    EMPTY_REQUEST_BODY = 'Отсутствует тело запроса'

    ORIGINAL_URL_NOT_IN_REQUEST = '\"url\" является обязательным полем!'
    ORIGINAL_URL_WRONG_FORMAT = 'Неправильной формат исходного URL'

    SHORT_URL_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
    SHORT_URL_WRONG_FORMAT = 'Указано недопустимое имя для короткой ссылки'
    SHORT_URL_SHORTER_THEN_LENGTH = (
        f'Короткая ссылка не должна быть длиннее {SHORT_URL_MAX_LENGTH}'
    )
    SHORT_URL_NOT_IN_DB = 'Указанный id не найден'


class InvalidAPIUsage(Exception):
    """Describes exception for invalid API usage."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code: HTTPStatus = None) -> None:
        """Initialize InvalidAPIUsage class object."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        """Turn error message to dict."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error) -> Tuple[Response, HTTPStatus]:
    """Handle invalid API usage exception."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error) -> Tuple[str, HTTPStatus]:
    """Handle page not found exception."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error) -> Tuple[str, HTTPStatus]:
    """Handle internal error exception."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
