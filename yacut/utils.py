"""
Describe utils functions for YaCut app.

This functions can't be related to other
modules and can be reused independently.
"""
import random
import string

from yacut.models import URLMap


def get_unique_short_id(string_length: int) -> str:
    """
    Generate random URL of random symbols.

    - Uppercase latin letters
    - Lowercase latin letters
    - Digits from 0 to 9
    """
    while True:
        generated_url = ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits,
            )
            for _ in range(string_length)
        )
        if not URLMap.query.filter_by(short=generated_url).first():
            break

    return generated_url
