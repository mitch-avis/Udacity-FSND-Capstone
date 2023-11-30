import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

from capstone_app.config.auth_config import auth_config
from capstone_app.errors.views import APIError

AUTH0_CONFIG = auth_config["AUTH0"]
DOMAIN = AUTH0_CONFIG["DOMAIN"]
ALGORITHMS = [AUTH0_CONFIG["ALGORITHMS"]]
AUDIENCE = AUTH0_CONFIG["AUDIENCE"]

BAD_REQUEST = ["Bad Request", 400]
UNAUTHORIZED = ["Unauthorized", 401]
FORBIDDEN = ["Forbidden", 403]


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header."""
    auth = request.headers.get("Authorization", None)
    if not auth:
        value = "authorization_header_missing"
        message = "Authorization header is expected."
        raise APIError(UNAUTHORIZED, value, message)
    parts = auth.split()
    if parts[0].lower() != "bearer":
        value = "invalid_header"
        message = 'Authorization header must start with "Bearer".'
        raise APIError(UNAUTHORIZED, value, message)
    if len(parts) == 1:
        value = "invalid_header"
        message = "Token not found."
        raise APIError(UNAUTHORIZED, value, message)
    if len(parts) > 2:
        value = "invalid_header"
        message = "Authorization header must be Bearer token."
        raise APIError(UNAUTHORIZED, value, message)
    token = parts[1]
    return token


def verify_decode_jwt(token):
    """verify_decode_jwt"""
    with urlopen(f"https://{DOMAIN}/.well-known/jwks.json") as jsonurl:
        jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        value = "invalid_header"
        message = "Authorization malformed."
        raise APIError(BAD_REQUEST, value, message)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            auth0_domain = f"https://{DOMAIN}/"
            payload = jwt.decode(
                token, rsa_key, algorithms=ALGORITHMS, audience=AUDIENCE, issuer=auth0_domain
            )
            return payload
        except jwt.ExpiredSignatureError as exc:
            value = "token_expired"
            message = "Token expired."
            raise APIError(UNAUTHORIZED, value, message) from exc
        except jwt.JWTClaimsError as exc:
            value = "invalid_claims"
            message = "Incorrect claims. Please, check the audience and issuer."
            raise APIError(UNAUTHORIZED, value, message) from exc
        except Exception as exc:
            value = "invalid_header"
            message = "Unable to parse authentication token."
            raise APIError(BAD_REQUEST, value, message) from exc
    value = "invalid_header"
    message = "Unable to find the appropriate key."
    raise APIError(BAD_REQUEST, value, message)


def check_permissions(permissions, payload):
    """check_permissions"""
    if "permissions" not in payload:
        value = "invalid_claims"
        message = "Permissions not included in JWT."
        raise APIError(BAD_REQUEST, value, message)
    if permissions not in payload["permissions"]:
        value = "forbidden"
        message = "Permission not found."
        raise APIError(FORBIDDEN, value, message)
    return True


def requires_auth(permissions=""):
    """requires_auth decorator method"""

    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permissions, payload)
            return func(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
