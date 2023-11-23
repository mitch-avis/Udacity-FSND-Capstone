from flask import Blueprint, jsonify

from capstone_app import log
from capstone_app.env_config import Config

EXCITED = Config.EXCITED


bp = Blueprint("routes", __name__)


@bp.route("/")
def get_greeting():
    greeting = {}
    greeting["greeting"] = "Hello"
    if EXCITED:
        greeting["greeting"] = greeting + "!!!!! You are doing great in this Udacity project."
    log.debug("greeting: %s", greeting["greeting"])
    return jsonify(greeting)


@bp.route("/coolkids")
def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"
