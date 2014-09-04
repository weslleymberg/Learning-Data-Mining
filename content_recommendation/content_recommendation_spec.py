import unittest
import os
from tempfile import NamedTemporaryFile
from should_dsl import should

from content_recommendation import Similar, sim, jaccardsim

def generate_temporary_file(data):
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(data)
    temp_file.close()
    return temp_file


class SimilarityFunctionsTest(unittest.TestCase):

    def it_should_return_the_similarity_between_two_sets(self):
        result = sim([5,0,0], [0,5,0])
        result |should| equal_to(0)
        result = sim([5,0,0], [4,0,0])
        result |should| equal_to(1)

    def it_should_return_the_jaccard_similarity_between_two_sets(self):
        result = jaccardsim({'Drama', 'Aventura'}, {'Aventura', 'Romance'})
        result |should| equal_to(round(1.0/3, 3))



class ContentRecommendationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ratings_file = generate_temporary_file("1::1193::5::978300760\n \
                                                    2::1357::5::978298709\n \
                                                    2::2268::5::978299297\n \
                                                    3::3421::4::978298147\n \
                                                    12::1193::4::978220179")

        cls.movies_file = generate_temporary_file("1193::One Flew Over the Cuckoo's Nest (1975)::Drama\n \
                                                   1357::Shine (1996)::Drama|Romance\n \
                                                   2268::Few Good Men, A (1992)::Crime|Drama\n \
                                                   3421::Animal House (1978)::Comedy")

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
        self.similar.movies |should| equal_to({'1193', '1357', '3421', '2268'})
        self.similar.ratings |should| equal_to({('1','1193'): 5, ('2', '1357'): 5, \
                                                ('3', '3421'): 4, ('12', '1193'): 4, \
                                                ('2', '2268'): 5})

    def it_should_normalize_the_ratings(self):
        self.similar.utility_matrix |should| equal_to({('1', '1193'): round(15.0/4, 3), \
                                              ('2', '1357'): round(10.0/4, 3), \
                                              ('2', '2268'): round(10.0/4, 3), \
                                              ('3', '3421'): round(3.0, 3), \
                                              ('12', '1193'): round(3.0, 3)})

    def it_should_generate_ratings_for_each_user(self):
        result = self.similar._get_ratings('1')
        result |should| equal_to([0, round(15.0/4, 3), 0, 0])
        result = self.similar._get_ratings('2')
        result |should| equal_to([0, 0, round(10.0/4, 3), round(10.0/4, 3)])
        result = self.similar._get_ratings('3')
        result |should| equal_to([round(3.0, 3), 0, 0, 0])
        result = self.similar._get_ratings('12')
        result |should| equal_to([0, round(3.0, 3), 0, 0])

    def it_should_keep_track_of_users_average_rate(self):
        self.similar.average_rate_by_user |should| equal_to({'1': round(5.0/4, 3), \
                                                             '2': round(10.0/4, 3), \
                                                             '3': round(4.0/4, 3), \
                                                             '12': round(4.0/4, 3)})


    def it_should_return_the_k_more_similar_users(self):
        similar_users = self.similar.get_k_more_similar_users(2)
        similar_users |should| equal_to(['1', '12'])

    def it_should_load_the_movies_file(self):
        self.similar.load_movies(self.movies_file.name)
        self.similar.movie_genres |should| equal_to({'1193':{'Drama'}, \
                                                     '1357':{'Drama', 'Romance'}, \
                                                     '2268':{'Crime', 'Drama'}, \
                                                     '3421':{'Comedy'}})

    def it_should_return_the_k_more_similar_movies(self):
        self.similar.load_movies(self.movies_file.name)
        similar_movies = self.similar.get_k_more_similar_movies(2)
        similar_movies |should| equal_to(['2268', '1357'])
