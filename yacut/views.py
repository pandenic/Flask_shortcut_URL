"""Contains view funstions for the YaCut app."""
from http import HTTPStatus

from flask import Response, abort, flash, redirect, render_template, url_for
from settings import INDEX_PAGE, SHORT_URL_DEFAULT_LENGTH, HTTPMethods

from yacut import app, db
from yacut.error_handlers import ErrorMessages
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=[HTTPMethods.GET, HTTPMethods.POST])
def index_view() -> str:
    """Describe index page view."""
    form = URLMapForm()
    if form.validate_on_submit():
        if (
            form.custom_id.data
            and URLMap.query.filter_by(short=form.custom_id.data).first()
        ):
            flash(ErrorMessages.SHORT_URL_EXISTS)
            return render_template(INDEX_PAGE, form=form)
        if not form.custom_id.data:
            form.custom_id.data = get_unique_short_id(SHORT_URL_DEFAULT_LENGTH)
        url_map = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url_map)
        db.session.commit()
        flash(
            f'Короткая ссылка '
            f'{url_for(index_view.__name__, _external=True)}'
            f'{form.custom_id.data}',
        )
        return render_template(INDEX_PAGE, form=form)
    return render_template(INDEX_PAGE, form=form)


@app.route('/<string:short_url>', methods=[HTTPMethods.GET])
def redirect_view(short_url: str) -> Response:
    """Describe redirection to original URL from short URL."""
    if not short_url.lower().isalnum():
        abort(404)
    url_to_redirect = URLMap.query.filter_by(short=short_url).first()
    if not url_to_redirect:
        abort(404)
    return redirect(url_to_redirect.original, code=HTTPStatus.FOUND)
