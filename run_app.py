#!/usr/bin/env python
from waitress import serve

from capstone_app import create_app, log
from capstone_app.config.env_config import Config


def main():
    app = create_app()
    DEBUG = Config.FLASK_DEBUG
    HOST = Config.HOST
    PORT = Config.PORT

    if not DEBUG:
        print(f"Serving {app.name} on {HOST}:{PORT}...")
        serve(app, host=HOST, port=PORT)
    else:
        log.warning("Running %s in debug mode on %s:%s...", app.name, HOST, PORT)
        app.run(host=HOST, port=PORT, debug=DEBUG, ssl_context="adhoc")


if __name__ == "__main__":
    main()
