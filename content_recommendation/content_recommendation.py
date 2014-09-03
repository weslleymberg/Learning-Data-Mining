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
