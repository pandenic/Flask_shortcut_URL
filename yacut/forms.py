"""Contains forms descriptions for the YaCut app."""
from flask_wtf import FlaskForm
from settings import SHORT_URL_REGEX_PATTERN
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from yacut.error_handlers import ErrorMessages


class URLMapForm(FlaskForm):
    """Describe a form for a shortening link."""

    original_link = URLField(
        'Укажите URL для сокращения.',
        validators=[
            DataRequired(message=ErrorMessages.ORIGINAL_URL_NOT_IN_REQUEST),
            URL(message=ErrorMessages.ORIGINAL_URL_WRONG_FORMAT),
        ],
    )
    custom_id = StringField(
        'Write in custom id (if you want)',
        validators=[
            Optional(),
            Length(
                max=16, message=ErrorMessages.SHORT_URL_SHORTER_THEN_LENGTH,
            ),
            Regexp(
                SHORT_URL_REGEX_PATTERN,
                message=ErrorMessages.SHORT_URL_WRONG_FORMAT,
            ),
        ],
    )
    submit = SubmitField('Create')
