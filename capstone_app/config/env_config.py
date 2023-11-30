from os import getenv


class Config:
    # pylint: disable=R0903
    FLASK_APP = getenv("FLASK_APP", "udacity_fsnd_capstone")
    FLASK_DEBUG = getenv("FLASK_DEBUG", "False").lower() in ("true", "t", "1")
    HOST = getenv("HOST", "0.0.0.0")
    PORT = getenv("PORT", "8080")
    ALLOWED_ORIGINS = getenv("ALLOWED_ORIGINS", "*")
    DB_PATH = getenv("DB_PATH", None)
    DB_USER = getenv("DB_USER", "postgres")
    DB_PASSWORD = getenv("DB_PASSWORD", "")
    DB_HOST = getenv("DB_HOST", "127.0.0.1")
    DB_PORT = getenv("DB_PORT", "5432")
    DB_NAME = getenv("DB_NAME", "capstone")
    AUTH0_DOMAIN = getenv("AUTH0_DOMAIN", "dev-5txjjo1g1jpy427b.us.auth0.com")
    ALGORITHMS = getenv("ALGORITHMS", "RS256")
    API_AUDIENCE = getenv("DB_NAME", "capstone")
