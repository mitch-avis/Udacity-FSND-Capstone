from flask import Blueprint

from capstone_app import log
from capstone_app.env_config import Config

EXCITED = Config.EXCITED


bp = Blueprint("routes", __name__)

DEBUG = Config.FLASK_DEBUG
if DEBUG:
    config = Config()
    env_vars = [
        env_var
        for env_var in dir(config)
        if not callable(getattr(config, env_var)) and not env_var.startswith("__")
    ]
    for env_var in env_vars:
        log.debug("%s=%s", env_var, getattr(config, env_var))


@bp.route("/")
def get_greeting():
    greeting = "Hello"
    log.debug("greeting: %s", greeting)
    if EXCITED:
        greeting = greeting + "!!!!! You are doing great in this Udacity project."
    return greeting


@bp.route("/coolkids")
def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"
