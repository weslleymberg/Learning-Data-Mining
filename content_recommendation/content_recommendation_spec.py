import unittest
import os
from tempfile import NamedTemporaryFile
from should_dsl import should

from content_recommendation import load_ratings

def generate_temporary_file(data):
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(data)
    temp_file.close()
    return temp_file

class ContentRecommendationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ratings_file = generate_temporary_file("1::1193::5::978300760")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.ratings_file.name)

    def it_should_load_user_ratings(self):
        result = load_ratings(self.ratings_file.name)
        result |should| equal_to({('1', '1193'): 5})
