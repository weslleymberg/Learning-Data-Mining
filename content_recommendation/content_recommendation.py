from itertools import product
from collections import defaultdict

def load_ratings(file_):
    users = set()
    movies = set()
    ratings = {}
    with open(file_) as f:
        for line in f:
            user_id, movie_id, rating, _ = line.strip().split("::")
            users.add(user_id)
            movies.add(movie_id)
            ratings[(user_id, movie_id)] = int(rating)
    return (users, movies, ratings)

def normalize_data(users, movies, ratings_table):
    scores = defaultdict(lambda: 0)
    normalized_table = {}
    for i in product(users, movies):
        u_id, m_id = i
        try:
            scores[u_id] += ratings_table[i]
        except KeyError:
            scores[u_id] += 0
    for key, value in ratings_table.iteritems():
        user_id, _ = key
        normalized_table[key] = round(ratings_table[key] - (float(scores[user_id])/len(movies)), 3)
    return normalized_table
