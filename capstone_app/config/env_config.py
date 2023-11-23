from os import getenv


class Config:
    # pylint: disable=R0903
    ALGORITHMS = ["RS256"]
    ALLOWED_ORIGINS = getenv("ALLOWED_ORIGINS", "*")
    API_AUDIENCE = getenv("DB_NAME", "capstone")
    AUTH0_DOMAIN = getenv("AUTH0_DOMAIN", "dev-5txjjo1g1jpy427b.us.auth0.com")
    DB_HOST = getenv("DB_HOST", "127.0.0.1")
    DB_NAME = getenv("DB_NAME", "capstone")
    DB_PASSWORD = getenv("DB_PASSWORD", "")
    DB_PORT = getenv("DB_PORT", "5432")
    DB_USER = getenv("DB_USER", "postgres")
    EXCITED = getenv("EXCITED", "False").lower() in ("true", "t", "1")
    FLASK_APP = getenv("FLASK_APP", "udacity_fsnd_capstone")
    FLASK_DEBUG = getenv("FLASK_DEBUG", "False").lower() in ("true", "t", "1")
    FLASK_ENV = getenv("FLASK_ENV", "production")
    HOST = getenv("HOST", "0.0.0.0")
    PORT = getenv("PORT", "8080")
    TESTING = getenv("TESTING", "False").lower() in ("true", "t", "1")
