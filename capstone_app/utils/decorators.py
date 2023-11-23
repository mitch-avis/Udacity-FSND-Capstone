from functools import wraps

from flask import redirect, session, url_for


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def requires_auth(func):
    """Use on routes that require a valid session, otherwise it aborts with a 403"""

    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return decorated
