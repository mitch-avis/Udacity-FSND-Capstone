from flask import Blueprint, jsonify

from capstone_app import log  # pylint: disable=R0401
from capstone_app.config.env_config import Config

EXCITED = Config.EXCITED


api = Blueprint("api", __name__)


@api.route("/")
def get_greeting():
    greeting = "Hello"
    response = {}
    response["greeting"] = greeting
    if EXCITED:
        response["greeting"] = f"{greeting}!!!!! You are doing great in this Udacity project."
    log.debug("greeting: %s", response["greeting"])
    return jsonify(response)


@api.route("/coolkids")
def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"
