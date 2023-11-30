from flask import Blueprint

from capstone_app import log  # pylint: disable=R0401
from capstone_app.auth.decorators import requires_auth
from capstone_app.config.env_config import Config

EXCITED = Config.EXCITED


api_bp = Blueprint("api", __name__, template_folder="templates")


@api_bp.route("/")
def home():
    """Home endpoint."""
    greeting = "Hello"
    if EXCITED:
        greeting = f"{greeting}!!!!! You are doing great in this Udacity project."
    log.debug("greeting: %s", greeting)
    return greeting


@api_bp.route("/coolkids")
def be_cool():
    """Some other endpoint."""
    return "Be cool, man, be coooool! You're almost a FSND grad!"


@api_bp.route("/admin")
@requires_auth
def admin():
    """Protected endpoint."""
    return "test"
