from itertools import product, combinations
from collections import defaultdict
from math import sqrt

def load_from_file(file_name):
    with open(file_name) as f:
        for line in f:
            yield line

def sim(a, b):
    def multiply(x, y):
        return x*y
    def sum_squared(y):
        return sum(map(lambda x: x*x, y))
    vd = sum(map(multiply, a, b))
    vdd = sqrt(sum_squared(a))*sqrt(sum_squared(b))
    return vd/vdd


class Similar(object):
    def __init__(self):
        self.users = set()
        self.movies = set()
        self.ratings = {}
        self.utility_matrix = {}

    def load_ratings(self, file_name):
        for line in load_from_file(file_name):
            user_id, movie_id, rating, _ = line.strip().split("::")
            self.users.add(user_id)
            self.movies.add(movie_id)
            self.ratings[(user_id, movie_id)] = int(rating)

    def normalize_data(self):
        scores = defaultdict(lambda: 0)
        for i in product(self.users, self.movies):
            u_id, m_id = i
            try:
                scores[u_id] += self.ratings[i]
            except KeyError:
                scores[u_id] += 0
        for key, value in self.ratings.iteritems():
            user_id, _ = key
            self.utility_matrix[key] = round(value - (float(scores[user_id])/len(self.movies)), 3)

    def _get_ratings(self, user_id):
        user_ratings = []
        for i in product((user_id,), self.movies):
            try:
                rate = self.utility_matrix[i]
            except KeyError:
                rate = 0
            user_ratings.append(rate)
        return user_ratings

    def get_k_more_similar_users(self, k):
        similars = []
        more_similars = set()
        for a, b in combinations(self.users, 2):
            ratings_a = self._get_ratings(a)
            ratings_b = self._get_ratings(b)
            similars.append(((a, b), sim(ratings_a, ratings_b)))
        sorted_similars = sorted(similars, key=lambda x: x[1], reverse=True)
        for user_pair, _ in sorted_similars:
            for i in user_pair:
                if len(more_similars) == k:
                    break
                more_similars.add(i)
        return list(more_similars)


if __name__ == '__main__':
    from datetime import datetime
    startTime = datetime.now()
    similar = Similar()
    print 'Loading data from file...'
    similar.load_ratings('ratings_sample.dat')
    print 'Normalazing data...'
    similar.normalize_data()
    print '>>Done initial processing in ', datetime.now()-startTime
    print 'Calculating similarities...'
    print similar.get_k_more_similar_users(3)
    print 'Finished in ', datetime.now()-startTime
