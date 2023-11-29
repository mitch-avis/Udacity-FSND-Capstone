# import json
import unittest
from datetime import date

from capstone_app import create_app
from capstone_app.config.env_config import Config


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        config_class = Config
        config_class.DB_NAME = "capstone_test"
        self.app = create_app(config_class)
        self.client = self.app.test_client
        self.test_movie = {
            "title": "Fight Club",
            "release_date": date(1999, 10, 15),
            "cast": ["Brad Pitt", "Edward Norton"],
        }
        self.test_actor = {
            "name": "Brad Pitt",
            "age": 59,
            "gender": "male",
        }

    def tearDown(self):
        """Executed after reach test"""

    def test_basic(self):
        response = self.client().get("/")
        actual = response.data.decode("utf-8")

        expected = "Hello"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual, expected)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
