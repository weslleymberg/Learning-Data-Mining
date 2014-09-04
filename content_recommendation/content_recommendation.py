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

def jaccardsim(a, b):
    return round(len(a.intersection(b))/float(len(a.union(b))), 3)


class Similar(object):
    def __init__(self):
        self.users = set()
        self.movies = set()
        self.movie_genres = {}
        self.ratings = {}
        self.utility_matrix = {}
        self.average_rate_by_user = {}
        self.average_rate_by_movie = {}

    def load_ratings(self, file_name):
        for line in load_from_file(file_name):
            user_id, movie_id, rating, _ = line.strip().split("::")
            self.users.add(user_id)
            self.movies.add(movie_id)
            self.ratings[(user_id, movie_id)] = int(rating)

    def load_movies(self, file_name):
        for line in load_from_file(file_name):
            movie_id, _, genre = line.strip().split("::")
            self.movie_genres[movie_id] = set(genre.split("|"))

    def normalize_data(self):
        user_scores = defaultdict(lambda: 0)
        movie_scores = defaultdict(lambda: 0)
        for i in product(self.users, self.movies):
            u_id, m_id = i
            try:
                rating = self.ratings[i]
                user_scores[u_id] += rating
                movie_scores[m_id] += rating
            except KeyError:
                user_scores[u_id] += 0
                movie_scores[m_id] += 0
        for key, value in self.ratings.iteritems():
            user_id, movie_id = key
            user_avg = (float(user_scores[user_id])/len(self.movies))
            movie_avg = (float(movie_scores[movie_id])/len(self.users))
            self.utility_matrix[key] = round(value - user_avg, 3)
            self.average_rate_by_user[user_id] = round(user_avg, 3)
            self.average_rate_by_movie[movie_id] = round(movie_avg, 3)

    def _get_ratings(self, id_, movie=False):
        user_ratings = []
        if movie:
            sequence = list(product((id_, ), self.users))
        else:
            sequence = product((id_, ), self.movies)
        for i in sequence:
            if movie: i = i[::-1]
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

    def get_k_more_similar_movies(self, k):
        similars = []
        more_similars = set()
        for a, b in combinations(self.movies, 2):
            ratings_a = self._get_ratings(a, movie=True)
            ratings_b = self._get_ratings(b, movie=True)
            similarity = sim(ratings_a, ratings_b)
            jaccard_similarity = jaccardsim(self.movie_genres[a], self.movie_genres[b])
            similars.append(((a, b), (similarity+jaccard_similarity)/2))
        sorted_similars = sorted(similars, key=lambda x: x[1], reverse=True)
        for movie_pair, _ in sorted_similars:
            for i in movie_pair:
                if len(more_similars) == k:
                    break
                more_similars.add(i)
        return list(more_similars)

    def calculate_average_rating(self, sequence, movie=False):
        total = 0
        if movie:
            dict_ = self.average_rate_by_movie
        else:
            dict_ = self.average_rate_by_user
        for i in sequence:
            total += dict_[i]
        return float(total)/len(sequence)


if __name__ == '__main__':
    from datetime import datetime
    startTime = datetime.now()
    similar = Similar()
    print 'Loading data from file...'
    similar.load_ratings('ratings_sample.dat')
    similar.load_movies('movies.dat')
    print 'Normalazing data...'
    similar.normalize_data()
    print '>>Done initial processing in ', datetime.now()-startTime
    print "================================================="

    print 'Calculating users similarities...'
    more_similar_users = similar.get_k_more_similar_users(3)
    u_avg = similar.calculate_average_rating(more_similar_users)
    print 'Average rating for the %i most similar users: %.5f' %(len(more_similar_users), u_avg)
    print '>>Finished in: ', datetime.now()-startTime
    print "================================================="

    print 'Calculating movies similarities...'
    more_similar_movies = similar.get_k_more_similar_movies(3)
    m_avg = similar.calculate_average_rating(more_similar_movies, movie=True)
    print 'Average rating for the %i most similar movies: %.5f' %(len(more_similar_movies),m_avg)
    print '>>Finished in: ', datetime.now()-startTime

    print "================================================="
    print "Total average: ", (u_avg+m_avg)/2
