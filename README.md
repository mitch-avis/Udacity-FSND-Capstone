# Udacity-FSND-Capstone

## Capstone Project for Udacity Full Stack Web Developer Nanodegree

Render Link: <https://TBD>

## Getting Started

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in
   the [python
   docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Virtual Environment** - It is recommended to work within a virtual environment whenever using
   Python for projects. This keeps your dependencies for each project separate and organized.
   Instructions for setting up a virual environment for your platform can be found in the [python
   docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required
   dependencies by navigating to the `/backend` directory and running:

   ```bash
   pip install -r requirements.txt
   ```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is
  required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the
  lightweight SQL database. You'll primarily work in `__init__.py` and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle
  cross-origin requests from the frontend server.

### Set up the Database

With Postgres running, create a `capstone` database:

```bash
createdb capstone
```

Populate the database using the `capstone_app/database/capstone.psql` file provided:

```bash
psql -U postgres -d capstone -f capstone_app/database/capstone.sql
```

### Run the Server

Before running the application locally, first ensure you are working within your created virtual
environment:

Also, in `capstone_app/__init__.py`, uncomment line 49: `db_drop_and_create_all()` on the initial
run to set up the required tables in the database.

To run the server, execute:

```bash
python run_app.py
```

By default, this will serve the application at `https://127.0.0.1:8080` with debug mode off. Debug
mode can be enabled by setting the `FLASK_DEBUG` environment variable:

```bash
export FLASK_DEBUG=True
```

List of all environment variables that can be set, with their default values:

```bash
ALGORITHMS="RS256"
ALLOWED_ORIGINS="*"
API_AUDIENCE="capstone"
AUTH0_DOMAIN="dev-5txjjo1g1jpy427b.us.auth0.com"
DB_HOST="127.0.0.1"
DB_NAME="capstone"
DB_PASSWORD=""
DB_PORT="5432"
DB_USER="postgres"
FLASK_APP="udacity_fsnd_capstone"
FLASK_DEBUG="False"
HOST="0.0.0.0"
PORT="8080"
TESTING="False"
```

## Testing

To initialize the test database, run the following commands:

```bash
dropdb capstone_test
createdb capstone_test
psql -U postgres -d capstone_test -f capstone_app/database/capstone.sql
```

(The first time you run the unit tests, omit the dropdb command.)

To run the tests (using pytest with code coverage enabled):

```bash
pytest --cov-report term-missing --cov
```

## API Reference

Authentication: This application requires authentication to perform various actions. All the
endpoints (except the root/home endpoint) require various permissions, which are passed via the
`Bearer` token.

Roles:

- Casting Assistant
  - Can view actors and movies
  - Permissions:
    - `get:actors`
    - `get:actor-by-id`
    - `get:movies`
    - `get:movie-by-id`
- Casting Director
  - Has all permissions a Casting Assistant has, plus...
  - Can add or delete an actor from the database
  - Can modify actors and movies
  - Permissions:
    - `get:actors`
    - `get:actor-by-id`
    - `get:movies`
    - `get:movie-by-id`
    - `patch:actor`
    - `patch:movie`
    - `post:actor`
    - `post:movie`
- Executive Producer
  - Has all permissions a Casting Director has, plus...
  - Can add or delete a movie from the database
  - Permissions:
    - `get:actors`
    - `get:actor-by-id`
    - `get:movies`
    - `get:movie-by-id`
    - `patch:actor`
    - `patch:movie`
    - `post:actor`
    - `post:movie`
    - `delete:actor`
    - `delete:movie`

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "code": 403,
    "error": "Forbidden",
    "message": {
        "message": "Permission not found.",
        "value": "forbidden"
    }
}
```

The API will return the following errors based on how the request fails:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

### Endpoints

#### GET /

- General
  - Root/Home endpoint
  - Public endpoint; does not require authentication
- Example Request:
  - `https://TBD`

<details>
    <summary>Example Response</summary>

```json
{
    "message": "Welcome!",
    "success": true
}
```

</details>

#### GET /actors

- General
  - Gets the list of all actors
  - Requires `get:actors` permission
- Example Request:
  - `https://TBD/actors`

<details>
    <summary markdown="span">Example Response</summary>

```json
{
    "actors": [
        {
            "id": 1,
            "name": "Brad Pitt"
        },
        {
            "id": 2,
            "name": "Edward Norton"
        }
    ],
    "success": true
}
```

</details>

#### GET /actors/{actor_id}

- General
  - Gets an actor's info using their ID
  - Requires `get:actor-by-id` permission
- Example Request:
  - `https://TBD/actors/1`

<details>
    <summary>Example Response</summary>

```json
{
    "actor": {
        "age": 59,
        "gender": "male",
        "id": 1,
        "name": "Brad Pitt"
    },
    "success": true
}
```
  
</details>

#### POST /actors

- General
  - Creates a new actor
  - Requires `post:actor` permission
- Request Body
  - name: string, required
  - age: number, required
  - gender: string, required
- Example Request:
  - `https://TBD/actors`
  - Request Body:

     ```json
        {
            "name": "Edward Norton",
            "age": "54",
            "gender": "male"
        }
     ```

<details>
    <summary>Example Response</summary>

```json
{
    "created_actor_id": 2,
    "success": true
}
```
  
</details>

#### PATCH /actors/{actor_id}

- General
  - Updates the specified actor's information
  - Requires `patch:actor` permission
- Request Body (at least one of the following fields is required):
  - name: string, optional
  - age: number, optional
  - gender: string, optional
- Example Request:
  - `https://TBD/actors/2`
  - Request Body:

     ```json
       {
            "age": "59"
       }
     ```

<details>
    <summary>Example Response</summary>

```json
{
    "actor": {
        "age": 59,
        "gender": "male",
        "id": 2,
        "name": "Edward Norton"
    },
    "success": true
}
```
  
</details>

#### DELETE /actors/{actor_id}

- General
  - Deletes the actor
  - Requires `delete:actor` permission
  - Will also delete the actor_in_movie link for that actor, thus removing them from the cast list
    of any movie they were previously in
- Example Request:
  - `https://TBD/actors/2`

<details>
    <summary>Example Response</summary>

```json
{
    "deleted_actor_id": 2,
    "success": true
}
```
  
</details>

#### GET /movies

- General
  - Gets the list of all movies
  - Requires `get:movies` permission
- Example Request:
  - `https://TBD/movies`

<details>
    <summary>Example Response</summary>

```json
{
    "movies": [
        {
            "id": 1,
            "title": "Fight Club"
        }
    ],
    "success": true
}
```

</details>

#### GET /movies/{movie_id}

- General
  - Gets an movie's info using its ID
  - Requires `get:movie-by-id` permission
- Example Request:
  - `https://TBD/movies/2`

<details>
<summary>Example Response</summary>

```json
{
    "movie": {
        "cast": [
            "Brad Pitt",
            "Edward Norton"
        ],
        "id": 2,
        "release_date": "October 15, 1999",
        "title": "Fight Club"
    },
    "success": true
}
```
  
</details>

#### POST /movies

- General
  - Creates a new movie
  - Requires `post:movie` permission
- Request Body:
  - title: string, required
  - release_date: date, required
  - cast: array of strings, non-empty, required (Note: Actors passed in the `cast` array in the
    request body must already exist in the database prior to making this request)
- Example Request:
  - `https://TBD/actors`
  - Request Body:

     ```json
        {
            "title": "Fight Club",
            "release_date": "10/15/1999",
            "cast": ["Brad Pitt", "Edward Norton"]
        }
     ```

<details>
    <summary>Example Response</summary>

```json
{
    "created_movie_id": 2,
    "success": true
}
```
  
</details>

#### PATCH /movie/{movie_id}

- General
  - Updates the specified movie's information
  - Requires `patch:movie` permission
- Request Body (at least one of the following fields must be present):
  - title: string, optional
  - release_date: date, optional
  - cast: array of string, non-empty, optional (Note: Actors passed in the `cast` array in the
    request body must already exist in the database prior to making this request)
- Example Request:
  - `https://TBD/movies/1`
  - Request Body:

     ```json
       {
            "cast": [
                "Brad Pitt",
                "Edward Norton"
            ]
        }
     ```

<details>
    <summary>Example Response</summary>

```json
{
    "movie": {
        "cast": [
            "Brad Pitt",
            "Edward Norton"
        ],
        "id": 1,
        "release_date": "October 15, 1999",
        "title": "Fight Club"
    },
    "success": true
}
```
  
</details>

#### DELETE /movies/{movie_id}

- General
  - Deletes the movie
  - Requires `delete:movie` permission
  - Will not affect the actors present in the database
- Example Request:
  - `https://TBD/movies/2`

<details>
    <summary>Example Response</summary>

```json
{
    "deleted_movie_id": 2,
    "success": true
}
```
  
</details>
