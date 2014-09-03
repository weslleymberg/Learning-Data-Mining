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
        cls.ratings_file = generate_temporary_file("1::1193::5::978300760\n \
                                                    2::1357::5::978298709\n \
                                                    3::3421::4::978298147\n \
                                                    12::1193::4::978220179")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.ratings_file.name)

    def it_should_load_user_ratings(self):
        users, movies, ratings = load_ratings(self.ratings_file.name)
        users |should| equal_to({'1', '2', '3', '12'})
        movies |should| equal_to({'1193', '1357', '3421'})
        ratings |should| equal_to({('1','1193'): 5, ('2', '1357'): 5, ('3', '3421'): 4, ('12', '1193'): 4})
