import unittest
import os
from tempfile import NamedTemporaryFile
from should_dsl import should

from content_recommendation import Similar, sim

def generate_temporary_file(data):
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(data)
    temp_file.close()
    return temp_file


class CosseneSimilarityTest(unittest.TestCase):

    def it_should_return_the_similarity_between_two_sets(self):
        result = sim([5,0,0], [0,5,0])
        result |should| equal_to(0)
        result = sim([5,0,0], [4,0,0])
        result |should| equal_to(1)


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

    def setUp(self):
        self.similar = Similar()
        self.similar.load_ratings(self.ratings_file.name)
        self.similar.normalize_data()

    def tearDown(self):
        del self.similar

    def it_should_load_user_ratings(self):
        self.similar.users |should| equal_to({'1', '2', '3', '12'})
        self.similar.movies |should| equal_to({'1193', '1357', '3421'})
        self.similar.ratings |should| equal_to({('1','1193'): 5, ('2', '1357'): 5, \
                                                ('3', '3421'): 4, ('12', '1193'): 4})

    def it_should_normalize_the_ratings(self):
        self.similar.utility_matrix |should| equal_to({('1', '1193'): round(10.0/3, 3), \
                                              ('2', '1357'): round(10.0/3, 3), \
                                              ('3', '3421'): round(8.0/3, 3), \
                                              ('12', '1193'): round(8.0/3, 3)})

    def it_should_generate_ratings_for_each_user(self):
        result = self.similar._get_ratings('1')
        result |should| equal_to([round(10.0/3, 3), 0, 0])
        result = self.similar._get_ratings('2')
        result |should| equal_to([0, round(10.0/3, 3), 0])
        result = self.similar._get_ratings('3')
        result |should| equal_to([0, 0, round(8.0/3, 3)])
        result = self.similar._get_ratings('12')
        result |should| equal_to([round(8.0/3, 3), 0, 0])


    def it_should_return_the_k_more_similar_users(self):
        similar_users = self.similar.get_k_more_similar_users(2)
        similar_users |should| equal_to(['1', '12'])
