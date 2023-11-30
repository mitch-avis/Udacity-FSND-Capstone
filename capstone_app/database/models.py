import json
from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String

from capstone_app.config.env_config import Config

if Config.DB_PATH is not None:
    db_path = Config.DB_PATH
else:
    DB_USER = Config.DB_USER
    DB_PASSWORD = Config.DB_PASSWORD
    DB_HOST = Config.DB_HOST
    DB_PORT = Config.DB_PORT
    DB_NAME = Config.DB_NAME
    db_path = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = SQLAlchemy()


def setup_db(app, database_path=db_path):
    """Binds a Flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """Drops the database tables and starts fresh. Can be used to initialize a clean database."""
    db.drop_all()
    db.create_all()
    # Add one demo row for each model to help with Postman tests
    actor_1 = Actor(
        name="Brad Pitt",
        age=59,
        gender="male",
    )
    actor_1.insert()
    actor_2 = Actor(
        name="Edward Norton",
        age=54,
        gender="male",
    )
    actor_2.insert()
    movie = Movie(
        title="Fight Club",
        release_date=date(1999, 10, 15),
    )
    movie.insert()


actor_in_movie = db.Table(
    "actor_in_movie",
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
)


class Movie(db.Model):
    """Movie Model"""

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    release_date = Column(Date, nullable=False)
    cast = db.relationship("Actor", secondary=actor_in_movie, backref="movies", lazy=True)

    def __init__(self, title, release_date):
        """Movie Constructor"""
        self.title = title
        self.release_date = release_date

    def insert(self):
        """Inserts a new movie into the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a movie from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a movie in the database"""
        db.session.commit()

    def short(self):
        """Short form representation of the movie model"""
        return {
            "id": self.id,
            "title": self.title,
        }

    def long(self):
        """Long form representation of the movie model"""
        return {
            "id": self.id,
            "title": self.title,
            "release_date": datetime.strftime(self.release_date, "%B %d, %Y"),
            "cast": [actor.name for actor in self.cast],
        }

    def __repr__(self):
        return json.dumps(self.short())


class Actor(db.Model):
    """Actor Model"""

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(128), nullable=False)

    def __init__(self, name, age, gender):
        """Actor Constructor"""
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        """Inserts a new actor into the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a actor from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a actor in the database"""
        db.session.commit()

    def short(self):
        """Short form representation of the actor model"""
        return {
            "id": self.id,
            "name": self.name,
        }

    def long(self):
        """Long form representation of the actor model"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

    def __repr__(self):
        return json.dumps(self.short())
