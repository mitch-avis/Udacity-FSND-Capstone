from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

from capstone_app import log  # pylint: disable=R0401

errors_bp = Blueprint("errors", __name__)


class APIException(Exception):
    error = "Internal Server Error"
    status_code = 500

    def __init__(self, error=None, value=str(), message=str()):
        super().__init__()
        if error is not None:
            self.error = error[0]
            self.status_code = error[1]
        self.value = value
        self.message = message

    def to_dict(self):
        response = {
            "error": self.error,
            "status_code": self.status_code,
            "detail": {
                "error": self.error,
                "value": self.value,
                "message": self.message,
            },
        }
        return response


@errors_bp.app_errorhandler(APIException)
def invalid_api_usage(error: APIException):
    log.debug(str(error.to_dict()))
    return jsonify(error.to_dict()), error.status_code


@errors_bp.app_errorhandler(Exception)
def handle_exception(error: Exception):
    if isinstance(error, HTTPException):
        status_code = error.code
        response = {
            "error": error.name,
            "status_code": status_code,
            "detail": error.description,
        }
    else:
        status_code = 500
        response = {
            "error": "Internal Server Error",
            "status_code": status_code,
            "detail": str(error),
        }
    log.debug(str(response))
    return jsonify(response), status_code
