"""Contains YaCut app model descriptions."""
from datetime import datetime, timezone

from settings import ORIGINAL_URL_MAX_LENGTH, SHORT_URL_MAX_LENGTH

from yacut import db


class URLMap(db.Model):
    """
    Contains URLMap model description.

    It is used to contain shortened and full URL link.
    """

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_URL_MAX_LENGTH),
        nullable=False,
        index=True,
        unique=True,
    )
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """Turn URLMap model object to dict."""
        return dict(
            original=self.original,
            short=self.short,
        )

    def from_dict(self, data: dict) -> None:
        """Set fields of URLMap model object from dict."""
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
