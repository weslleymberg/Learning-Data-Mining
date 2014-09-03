def load_ratings(file_):
    result = {}
    with open(file_) as f:
        for line in f:
            user_id, movie_id, rating, _ = line.split("::")
            result[(user_id, movie_id)] = int(rating)
    return result
