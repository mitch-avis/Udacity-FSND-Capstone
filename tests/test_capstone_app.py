import json
import unittest
from datetime import date

from capstone_app import create_app
from capstone_app.config.auth_config import auth_config
from capstone_app.config.env_config import Config


class CapstoneTestCase(unittest.TestCase):
    # pylint: disable=C0103,R0904
    """This class represents the capstone test case"""

    TOKENS = auth_config["TOKENS"]
    ASSISTANT_TOKEN = TOKENS["ASSISTANT"]
    DIRECTOR_TOKEN = TOKENS["DIRECTOR"]
    PRODUCER_TOKEN = TOKENS["PRODUCER"]
    VALID_ACTOR = {"name": "Edward Norton", "age": 54, "gender": "male"}
    INVALID_ACTOR = {"name": "Brad Pitt"}
    VALID_ACTOR_PATCH = {"age": 60}
    INVALID_ACTOR_PATCH = {}
    VALID_MOVIE = {"title": "Fight Club", "release_date": date(1999, 10, 15), "cast": ["Brad Pitt"]}
    INVALID_MOVIE = {"title": "Fight Club", "cast": ["Brad Pitt"]}
    VALID_MOVIE_PATCH = {"cast": ["Brad Pitt", "Edward Norton"]}
    INVALID_MOVIE_PATCH = {}

    def setUp(self):
        """Define test variables and initialize app."""
        config_class = Config
        config_class.DB_NAME = "capstone_test"
        self.app = create_app(config_class)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""

    def test_home(self):
        response = self.client().get("/")
        data = json.loads(response.data)
        actual = data["message"]

        expected = "Welcome!"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual, expected)

    def test_001_api_call_without_token_401(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"]["message"], "Authorization header is expected.")

    def test_002_get_actors_200(self):
        """Passing Test for GET /actors"""
        res = self.client().get(
            "/actors", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn("actors", data)
        self.assertTrue(len(data["actors"]))

    def test_003_get_actor_by_id_200(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get(
            "/actors/1", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("actor", data)
        self.assertIn("name", data["actor"])

    def test_004_get_actor_by_id_404(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get(
            "/actors/100", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_005_create_actor_with_assistant_token_403(self):
        """Failing Test for POST /actors"""
        res = self.client().post(
            "/actors",
            headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"},
            json=self.VALID_ACTOR,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_006_create_actor_201(self):
        """Passing Test for POST /actors"""
        res = self.client().post(
            "/actors",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.VALID_ACTOR,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn("created_actor_id", data)

    def test_007_create_actor_400(self):
        """Failing Test for POST /actors"""
        res = self.client().post(
            "/actors",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.INVALID_ACTOR,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_008_update_actor_info_200(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch(
            "/actors/1",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.VALID_ACTOR_PATCH,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("actor", data)
        self.assertEqual(data["actor"]["age"], self.VALID_ACTOR_PATCH["age"])

    def test_009_update_actor_info_400(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch(
            "/actors/1",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.INVALID_ACTOR_PATCH,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_010_delete_actor_with_assistant_token_403(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete(
            "/actors/1", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_011_delete_actor_200(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete(
            "/actors/2", headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("deleted_actor_id", data)

    def test_012_delete_actor_404(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete(
            "/actors/100", headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_013_get_movies_200(self):
        """Passing Test for GET /movies"""
        res = self.client().get(
            "/movies", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn("movies", data)
        self.assertTrue(len(data["movies"]))

    def test_014_get_movie_by_id_200(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get(
            "/movies/1", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("movie", data)
        self.assertIn("release_date", data["movie"])
        self.assertIn("cast", data["movie"])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_015_get_movie_by_id_404(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get(
            "/movies/100", headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_016_create_movie_with_assistant_token_403(self):
        """Failing Test for POST /movies"""
        res = self.client().post(
            "/movies",
            headers={"Authorization": f"Bearer {self.ASSISTANT_TOKEN}"},
            json=self.VALID_MOVIE,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_017_create_movie_201(self):
        """Passing Test for POST /movies"""
        res = self.client().post(
            "/movies",
            headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"},
            json=self.VALID_MOVIE,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn("created_movie_id", data)

    def test_018_create_movie_400(self):
        """Failing Test for POST /movies"""
        res = self.client().post(
            "/movies",
            headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"},
            json=self.INVALID_MOVIE,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_019_update_movie_info_200(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch(
            "/movies/1",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.VALID_MOVIE_PATCH,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("movie", data)
        self.assertEqual(data["movie"]["cast"], self.VALID_MOVIE_PATCH["cast"])

    def test_020_update_movie_info_400(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch(
            "/movies/1",
            headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"},
            json=self.INVALID_MOVIE_PATCH,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_021_delete_movie_with_director_token_403(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete(
            "/movies/3", headers={"Authorization": f"Bearer {self.DIRECTOR_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn("message", data)

    def test_022_delete_movie_200(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete(
            "/movies/1", headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("deleted_movie_id", data)

    def test_023_delete_movie_404(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete(
            "/movies/100", headers={"Authorization": f"Bearer {self.PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn("message", data)
