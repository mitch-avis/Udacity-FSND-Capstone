import dateparser
from flask import Blueprint, jsonify, request

from capstone_app import log  # pylint: disable=R0401
from capstone_app.auth.auth import requires_auth
from capstone_app.database.models import Actor, Movie, db
from capstone_app.errors.views import APIError

BAD_REQUEST = ["Bad Request", 400]
NOT_FOUND = ["Not Found", 404]
UNPROCESSABLE_CONTENT = ["Unprocessable Content", 422]


api_bp = Blueprint("api", __name__)


@api_bp.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
    return response


@api_bp.route("/")
def home():
    """Home endpoint."""
    greeting = "Welcome!"
    return (
        jsonify(
            {
                "success": True,
                "message": greeting,
            }
        ),
        200,
    )


@api_bp.route("/actors", methods=["GET"])
@requires_auth("get:actors")
def get_actors(payload):
    log.debug("payload: %s", payload)
    actors_results = db.session.query(Actor).order_by(Actor.id).all()
    actors = []
    for actor in actors_results:
        actors.append(actor.short())
    if not actors:
        value = ""
        message = "No actors found."
        raise APIError(NOT_FOUND, value, message)
    return (
        jsonify(
            {
                "success": True,
                "actors": actors,
            }
        ),
        200,
    )


@api_bp.route("/actors/<int:actor_id>", methods=["GET"])
@requires_auth("get:actor-by-id")
def get_actor_by_id(payload, actor_id):
    log.debug("payload: %s", payload)
    actor = db.session.get(Actor, actor_id)
    if not actor:
        value = actor_id
        message = f"No actor with actor_id [{actor_id}] found."
        raise APIError(NOT_FOUND, value, message)
    return (
        jsonify(
            {
                "success": True,
                "actor": actor.long(),
            }
        ),
        200,
    )


@api_bp.route("/actors", methods=["POST"])
@requires_auth("post:actor")
def create_actor(payload):
    log.debug("payload: %s", payload)
    request_body = request.get_json()
    if not request_body:
        message = "Missing request body."
        raise APIError(BAD_REQUEST, None, message)
    try:
        name = request_body["name"]
        age = request_body["age"]
        gender = request_body["gender"]
    except KeyError as exc:
        value = exc.args
        message = "New actor must have valid name, age, and gender."
        raise APIError(BAD_REQUEST, value, message) from exc
    if name == "":
        message = "Actor name cannot be blank."
        raise APIError(BAD_REQUEST, None, message)
    if age == "":
        message = "Actor age cannot be blank."
        raise APIError(BAD_REQUEST, None, message)
    if gender == "":
        message = "Actor gender cannot be blank."
        raise APIError(BAD_REQUEST, None, message)
    new_actor = Actor(name, age, gender)
    new_actor.insert()
    return (
        jsonify(
            {
                "success": True,
                "created_actor_id": new_actor.id,
            }
        ),
        201,
    )


@api_bp.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actor")
def update_actor(payload, actor_id):
    log.debug("payload: %s", payload)
    actor = db.session.get(Actor, actor_id)
    if not actor:
        value = actor_id
        message = f"No actor with actor_id [{actor_id}] found."
        raise APIError(NOT_FOUND, value, message)
    request_body = request.get_json()
    if not request_body:
        message = "Missing request body."
        raise APIError(BAD_REQUEST, None, message)
    if "name" in request_body:
        if request_body["name"] == "":
            message = "Actor name cannot be blank."
            raise APIError(BAD_REQUEST, None, message)
        actor.name = request_body["name"]
    if "age" in request_body:
        if request_body["age"] == "":
            message = "Actor age cannot be blank."
            raise APIError(BAD_REQUEST, None, message)
        actor.age = request_body["age"]
    if "gender" in request_body:
        if request_body["gender"] == "":
            message = "Actor gender cannot be blank."
            raise APIError(BAD_REQUEST, None, message)
        actor.gender = request_body["gender"]
    actor.update()
    return (
        jsonify(
            {
                "success": True,
                "actor": actor.long(),
            }
        ),
        200,
    )


@api_bp.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth("delete:actor")
def delete_actor(payload, actor_id):
    log.debug("payload: %s", payload)
    actor = db.session.get(Actor, actor_id)
    if not actor:
        value = actor_id
        message = f"No actor with actor_id [{actor_id}] found."
        raise APIError(NOT_FOUND, value, message)
    actor.delete()
    return (
        jsonify(
            {
                "success": True,
                "deleted_actor_id": actor.id,
            }
        ),
        200,
    )


@api_bp.route("/movies", methods=["GET"])
@requires_auth("get:movies")
def get_movies(payload):
    log.debug("payload: %s", payload)
    movies_results = db.session.query(Movie).order_by(Movie.id).all()
    movies = []
    for movie in movies_results:
        movies.append(movie.short())
    if not movies:
        value = ""
        message = "No movies found."
        raise APIError(NOT_FOUND, value, message)
    return (
        jsonify(
            {
                "success": True,
                "movies": movies,
            }
        ),
        200,
    )


@api_bp.route("/movies/<int:movie_id>", methods=["GET"])
@requires_auth("get:movie-by-id")
def get_movie_by_id(payload, movie_id):
    log.debug("payload: %s", payload)
    movie = db.session.get(Movie, movie_id)
    if not movie:
        value = movie_id
        message = f"No movie with movie_id [{movie_id}] found."
        raise APIError(NOT_FOUND, value, message)
    return (
        jsonify(
            {
                "success": True,
                "movie": movie.long(),
            }
        ),
        200,
    )


@api_bp.route("/movies", methods=["POST"])
@requires_auth("post:movie")
def create_movie(payload):
    log.debug("payload: %s", payload)
    request_body = request.get_json()
    if not request_body:
        message = "Missing request body."
        raise APIError(BAD_REQUEST, None, message)
    try:
        title = request_body["title"]
        release_date = request_body["release_date"]
        cast = request_body["cast"]
    except KeyError as exc:
        value = exc.args
        message = "New movie must have valid title, release_date, and cast."
        raise APIError(BAD_REQUEST, value, message) from exc
    if title == "":
        message = "Movie title cannot be blank."
        raise APIError(BAD_REQUEST, None, message)
    release_date = dateparser.parse(release_date)
    if not release_date:
        value = request_body["release_date"]
        message = "Invalid date format."
        raise APIError(BAD_REQUEST, value, message)
    release_date = release_date.date()
    if cast is None:
        message = "Movie requires cast (list of actors)."
        raise APIError(BAD_REQUEST, None, message)
    new_movie = Movie(title, release_date)
    actors = db.session.query(Actor).filter(Actor.name.in_(cast)).all()
    if len(cast) == len(actors):
        new_movie.cast = actors
        new_movie.insert()
    else:
        message = "Cast contains unknown/missing actors; add them first."
        raise APIError(UNPROCESSABLE_CONTENT, None, message)
    return (
        jsonify(
            {
                "success": True,
                "created_movie_id": new_movie.id,
            }
        ),
        201,
    )


@api_bp.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movie")
def update_movie(payload, movie_id):
    log.debug("payload: %s", payload)
    movie = db.session.get(Movie, movie_id)
    if not movie:
        value = movie_id
        message = f"No movie with movie_id [{movie_id}] found."
        raise APIError(NOT_FOUND, value, message)
    request_body = request.get_json()
    if not request_body:
        message = "Missing request body."
        raise APIError(BAD_REQUEST, None, message)
    if "title" in request_body:
        title = request_body["title"]
        if title == "":
            message = "Movie title cannot be blank."
            raise APIError(BAD_REQUEST, None, message)
        movie.title = title
    if "release_date" in request_body:
        release_date = dateparser.parse(request_body["release_date"])
        if not release_date:
            value = request_body["release_date"]
            message = "Invalid date format."
            raise APIError(BAD_REQUEST, value, message)
        movie.release_date = release_date.date()
    if "cast" in request_body:
        cast = request_body["cast"]
        if not cast:
            message = "Movie requires cast (list of actors)."
            raise APIError(BAD_REQUEST, None, message)
        actors = db.session.query(Actor).filter(Actor.name.in_(cast)).all()
        if len(cast) == len(actors):
            movie.cast = actors
        else:
            message = "Cast contains unknown/missing actors; add them first."
            raise APIError(UNPROCESSABLE_CONTENT, None, message)
    movie.update()
    return (
        jsonify(
            {
                "success": True,
                "movie": movie.long(),
            }
        ),
        200,
    )


@api_bp.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth("delete:movie")
def delete_movie(payload, movie_id):
    log.debug("payload: %s", payload)
    movie = db.session.get(Movie, movie_id)
    if not movie:
        value = movie_id
        message = f"No movie with movie_id [{movie_id}] found."
        raise APIError(NOT_FOUND, value, message)
    movie.delete()
    return (
        jsonify(
            {
                "success": True,
                "deleted_movie_id": movie.id,
            }
        ),
        200,
    )
