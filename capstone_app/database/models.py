from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String

from capstone_app.config.env_config import Config

DB_USER = Config.DB_USER
DB_PASSWORD = Config.DB_PASSWORD
DB_HOST = Config.DB_HOST
DB_PORT = Config.DB_PORT
DB_NAME = Config.DB_NAME

db_path = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = SQLAlchemy()


def setup_db(app, database_path=db_path):
    """Binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Person(db.Model):
    # pylint: disable=R0903
    """Person"""

    __tablename__ = "People"

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    catchphrase = Column(String)

    def __init__(self, name, catchphrase=""):
        self.name = name
        self.catchphrase = catchphrase

    def format(self):
        return {"id": self.id, "name": self.name, "catchphrase": self.catchphrase}
