from fastapi import HTTPException, status
from database.connector import DatabaseConnector
# 예진이가 추가한 부분
from surprise import Dataset, Reader, KNNWithMeans
from surprise import SVD, accuracy
from surprise.model_selection import train_test_split, GridSearchCV
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Movie Controllers


def get_movies(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return movies


def get_movie(id: int) -> dict:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		WHERE movie.movieId = %s
		""",
		(id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
	return movies[0]


def get_movie_rating(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.movieId = %s
		""",
		(movie_id),
	)
	if len(ratings) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
	return ratings


def get_average_rating(movie_id: int) -> float:
	database = DatabaseConnector()
	rating = database.query_get(
		"""
		SELECT
			AVG(ratings.ratingScore)
		AS average_rating
		FROM ratings
		WHERE ratings.movieId = %s
		""",
		(movie_id),
	)
	if len(rating) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ratings found for this movie")
	return rating[0]['average_rating']


def get_movie_genre(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		WHERE movie_genres.movieId = %s
		""",
		(movie_id),
	)
	if len(genres) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
	return genres


def search_movies(query: str, limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path
		FROM movie
		WHERE movie.movieTitle LIKE %s
		LIMIT %s OFFSET %s
		""",
		(f"%{query}%", limit, offset),
	)
	return movies


# User Controllers


def get_users(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	users = database.query_get(
		"""
		SELECT
			user.userId,
			user.age,
			user.gender,
			user.occupation,
			user.ZIPCODE
		FROM user
		LIMIT %s OFFSET %s;
		""",
		(limit, offset),
	)
	return users


def get_user(id: int) -> dict:
	database = DatabaseConnector()
	users = database.query_get(
		"""
		SELECT
			user.userId,
			user.age,
			user.gender,
			user.occupation,
			user.ZIPCODE
		FROM user
		WHERE user.userId = %s
		""",
		(id),
	)
	if len(users) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return users[0]


# 가장 최근에 평가한 영화 순서대로 목록이 출력되도록 수정함
def get_user_rated_movies(user_id: int) -> list[dict]:
	database = DatabaseConnector()
	movies = database.query_get(
		"""
		SELECT
			movie.movieId,
			movie.movieTitle,
			movie.releaseDate,
			movie.videoReleaseDate,
			movie.year, 
			movie.backdrop_path,
			movie.poster_path,
			ratings.ratingScore,
			ratings.timestamp
		FROM movie
		INNER JOIN ratings ON movie.movieId = ratings.movieId
		WHERE ratings.userId = %s
		ORDER BY ratings.timestamp DESC
		""",
		(user_id),
	)
	if len(movies) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
	return movies


# Genre Controllers


def get_genres(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return genres


def get_genre(movie_id: int) -> list[dict]:
	database = DatabaseConnector()
	genres = database.query_get(
		"""
		SELECT
			movie_genres.mgenreId,
			movie_genres.movieId,
			movie_genres.genre
		FROM movie_genres
		WHERE movie_genres.mgenreId = %s
		""",
		(movie_id),
	)
	if len(genres) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
	return genres



# Rating Controllers


def get_ratings(limit: int = 10, offset: int = 0) -> list[dict]:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		LIMIT %s OFFSET %s
		""",
		(limit, offset),
	)
	return ratings


def get_rating(id: int) -> dict:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.ratingId = %s
		""",
		(id),
	)
	if len(ratings) == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
	return ratings[0]


def get_user_movie_rating(user_id: int, movie_id: int) -> dict:
	database = DatabaseConnector()
	ratings = database.query_get(
		"""
		SELECT
			ratings.ratingId,
			ratings.userId,
			ratings.movieId,
			ratings.ratingScore,
			ratings.timestamp
		FROM ratings
		WHERE ratings.userId = %s AND ratings.movieId = %s
		""",
		(user_id, movie_id),
	)
	if len(ratings) == 0:
		return None
	return ratings[0]


# 예진이가 작성한 부분

# 필수1) 완료
# [필수]선택된 사용자와 같은 직업을 가진 사람들이 좋아하는 상위 10개의 영화 목록
def get_top_movies_by_occupation(user_id: int) -> dict:
    database = DatabaseConnector()
    # 사용자의 직업 가져오기
    user_occupation_result = database.query_get(
        """
        SELECT occupation
        FROM user
        WHERE userId = %s
        """,
        (user_id,)
    )
    if not user_occupation_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    occupation = user_occupation_result[0]['occupation']

    # 해당 직업을 가진 사람들이 좋아하는 상위 10개의 영화 목록 가져오기
    movies = database.query_get(
        """
        SELECT
            m.movieId,
			m.movieTitle,
            AVG(r.ratingScore) AS avg_rating,
            m.poster_path,
            m.backdrop_path
        FROM ratings r
        JOIN movie m ON r.movieId = m.movieId
        JOIN user u ON r.userId = u.userId
        WHERE u.occupation = %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
        ORDER BY avg_rating DESC
        LIMIT 10
        """,
        (occupation,)
    )
    if len(movies) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")

    return {
        "movies": movies,
        "occupation": occupation
    }



# 필수2) 완료
# [필수]선택된 사용자와 같은 나이의 사람들이 좋아하는 상위 10개의 영화 목록
def get_top_movies_by_age(user_id: int) -> dict:
    database = DatabaseConnector()
    # 사용자의 나이 가져오기
    user_age_result = database.query_get(
        """
        SELECT age
        FROM user
        WHERE userId = %s
        """,
        (user_id,)
    )
    if not user_age_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_age = user_age_result[0]['age']

    # 같은 나이의 사용자가 평가한 영화 중 상위 10개 영화 목록 가져오기
    movies = database.query_get(
        """
        SELECT
            m.movieId,
            m.movieTitle,
            AVG(r.ratingScore) AS avg_rating,
            m.poster_path,
            m.backdrop_path
        FROM ratings r
        JOIN movie m ON r.movieId = m.movieId
        JOIN user u ON r.userId = u.userId
        WHERE u.age = %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
        ORDER BY avg_rating DESC
        LIMIT 10
        """,
        (user_age,)
    )
    if len(movies) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
    
    return {
        "movies": movies,
        "user_age": user_age
    }


# 필수3) 완료
# [필수]사용자가 아직 보지 않은 KNN 기반 아이템 기반 협업 필터링 최고 평점 예측 영화 상위 10개 목록
def get_top_movies_by_knn(user_id: int) -> list[dict]:
    database = DatabaseConnector()
    
    # query_get을 사용하여 데이터 가져오기
    ratings = database.query_get(
        """
        SELECT 
            userId AS user, 
            movieId AS item, 
            ratingScore AS rating
        FROM ratings
        """,
        ()
    )
    
    # DataFrame으로 변환
    df = pd.DataFrame(ratings)
    
    # 열 이름을 변경하기
    df.columns = ['user', 'item', 'rating']
    
    # 'rating' 컬럼을 float으로 변환
    try:
        df['rating'] = df['rating'].astype(float)
    except ValueError as e:
        print(f"Error converting 'rating' to float: {e}")
        raise HTTPException(status_code=500, detail="Error converting 'rating' to float.")
    
    # Surprise data set으로 변환
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user', 'item', 'rating']], reader)
    
    # train, test data set으로 분할
    trainset, testset = train_test_split(data, test_size=.25)
    
    # KNNWithMeans 알고리즘 설정
    sim_options = {
        "name": "pearson",
        "user_based": False,  # Item-based collaborative filtering
    }
    algo = KNNWithMeans(k=40, sim_options=sim_options)
    
    # train
    algo.fit(trainset)
    
    # 사용자가 이미 본 영화 가져오기
    seen_movies = database.query_get(
        """
        SELECT movieId
        FROM ratings
        WHERE userId = %s
        """,
        (user_id,)
    )
    seen_movies = {row['movieId'] for row in seen_movies}
    
    # predict 및 상위 10개 추천
    all_movies = df['item'].unique()
    predictions = []
    
    for movie in all_movies:
        if movie not in seen_movies:
            predictions.append((movie, algo.predict(user_id, movie).est))
    
    top_10 = sorted(predictions, key=lambda x: x[1], reverse=True)[:10]
    
    if not top_10:
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    # 영화 정보 가져오기
    movie_ids = [int(movie) for movie, _ in top_10]  # Convert movie IDs to int
    movies_info = database.query_get(
        """
        SELECT movieId, movieTitle, poster_path, backdrop_path
        FROM movie
        WHERE movieId IN %s
        """,
        (tuple(movie_ids),)
    )
    
    movie_dict = {int(movie['movieId']): movie for movie in movies_info}  # Convert keys to int
    
    return [
        {
            "movieId": int(movie),  # Ensure movieId is an int
            "movieTitle": movie_dict[int(movie)]['movieTitle'],
            "rating": rating,
            "poster_path": movie_dict[int(movie)]['poster_path'],
            "backdrop_path": movie_dict[int(movie)]['backdrop_path']
        }
        for movie, rating in top_10
    ]






# 추가1) 완료
# [추가]최근 한 달 동안 가장 많이 평가된 영화 중에서 평균 평점이 가장 높은 상위 10개의 영화 목록 
def get_top_rated_movies_most_rated_last_month() -> list[dict]:
    database = DatabaseConnector()
    # ratings 테이블에서 가장 최근 날짜 가져오기
    recent_date_query = """
        SELECT MAX(timestamp) AS recent_date
        FROM ratings
    """
    recent_date_result = database.query_get(recent_date_query, ())
    
    if not recent_date_result or 'recent_date' not in recent_date_result[0]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ratings found")
    recent_date = recent_date_result[0]['recent_date']

    # 가장 최근 한 달 동안 가장 많이 평가된 영화 중에서 평균 평점이 가장 높은 상위 10개의 영화 가져오기
    movies = database.query_get(
        """
        SELECT
            m.movieId,
            m.movieTitle,
            m.poster_path,
            m.backdrop_path,
            AVG(r.ratingScore) AS avg_rating,
            COUNT(r.ratingId) AS rating_count
        FROM ratings r
        JOIN movie m ON r.movieId = m.movieId
        WHERE r.timestamp BETWEEN DATE_SUB(%s, INTERVAL 30 DAY) AND %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
        HAVING COUNT(r.ratingId) > 1
        ORDER BY rating_count DESC, avg_rating DESC
        LIMIT 10
        """,
        (recent_date, recent_date)
    )
    
    if len(movies) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
    
    return movies


# 추가2)
# [추가]사용자가 가장 많이 평가한 영화 장르에서 가장 높은 평균 평점을 받은 상위 10개의 영화 목록
def get_top_movies_by_favorite_genre(user_id: int) -> dict:
    database = DatabaseConnector()
    # 사용자가 가장 많이 평가한 장르 가져오기
    favorite_genre_result = database.query_get(
        """
        SELECT mg.genre, COUNT(r.ratingId) AS rating_count
        FROM ratings r
        JOIN movie_genres mg ON r.movieId = mg.movieId
        WHERE r.userId = %s
        GROUP BY mg.genre
        ORDER BY rating_count DESC
        LIMIT 1
        """,
        (user_id,)
    )
    
    if not favorite_genre_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No favorite genre found for user")

    favorite_genre = favorite_genre_result[0]['genre']

    # 해당 장르에서 가장 높은 평균 평점을 받은 상위 10개의 영화 가져오기
    movies = database.query_get(
        """
        SELECT m.movieId, m.movieTitle, AVG(r.ratingScore) AS avg_rating, m.poster_path, m.backdrop_path
        FROM ratings r
        JOIN movie m ON r.movieId = m.movieId
        JOIN movie_genres mg ON m.movieId = mg.movieId
        WHERE mg.genre = %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
        ORDER BY avg_rating DESC
        LIMIT 10
        """,
        (favorite_genre,)
    )
    
    if len(movies) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found in favorite genre")
    
    return {
        "movies": movies,
        "favorite_genre": favorite_genre
    }




# 추가3) 
# [추가]Content-Based Filtering을 사용하여 특정 영화의 장르를 기반으로 관련성이 높은 상위 10개의 영화 목록
def get_related_movies_by_genre(movie_id: int) -> dict:
    database = DatabaseConnector()
    
    # 특정 영화의 장르 가져오기
    genre_query = """
        SELECT genre
        FROM movie_genres
        WHERE movieId = %s
    """
    genres = database.query_get(genre_query, (movie_id,))
    genres = [row['genre'] for row in genres]
    if not genres:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genres not found for the movie")
    
    # 해당 장르의 모든 영화 가져오기
    related_movies_query = """
        SELECT DISTINCT m.movieId, m.movieTitle, GROUP_CONCAT(DISTINCT mg.genre ORDER BY mg.genre) as genres, m.poster_path, m.backdrop_path
        FROM movie m
        JOIN movie_genres mg ON m.movieId = mg.movieId
        WHERE mg.genre IN %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
    """
    related_movies = database.query_get(related_movies_query, (tuple(genres),))
    
    if not related_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No related movies found")

    # 데이터프레임으로 변환
    df = pd.DataFrame(related_movies)

    # 장르 정보 벡터화
    df['genres'] = df['genres'].apply(lambda x: x.split(','))
    df = df.explode('genres')
    df = pd.get_dummies(df, columns=['genres'], prefix='', prefix_sep='')

    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(df.drop(columns=['movieId', 'movieTitle', 'poster_path', 'backdrop_path']))
    
    # 입력 영화의 인덱스 찾기
    movie_idx = df[df['movieId'] == movie_id].index[0]
    
    # 유사도가 높은 영화 찾기
    similar_indices = cosine_sim[movie_idx].argsort()[::-1][1:11]
    similar_movies = df.iloc[similar_indices][['movieId', 'movieTitle', 'poster_path', 'backdrop_path']].drop_duplicates()

    result = similar_movies.to_dict(orient='records')

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recommendations found")
    return {
        "movies": result,
        "genres": genres
    }


# 추가4)
# [추가] 특정 장르에 해당하는 모든 영화를 평균 평점이 높은 순으로 출력하는 함수
def get_all_movies_by_genre_sorted_by_rating(genre: str) -> list[dict]:
    database = DatabaseConnector()

    # 해당 장르의 모든 영화 가져오기
    related_movies_query = """
        SELECT m.movieId, m.movieTitle, m.releaseDate, AVG(r.ratingScore) AS avg_rating, m.poster_path, m.backdrop_path
        FROM movie m
        JOIN movie_genres mg ON m.movieId = mg.movieId
        JOIN ratings r ON m.movieId = r.movieId
        WHERE mg.genre = %s
        GROUP BY m.movieId, m.movieTitle, m.poster_path, m.backdrop_path
        ORDER BY avg_rating DESC
    """
    related_movies = database.query_get(related_movies_query, (genre,))
    
    if not related_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found for this genre")

    return related_movies