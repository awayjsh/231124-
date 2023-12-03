from django.test import TestCase
import requests
import os

# Create your tests here.
import json

TMDB_API_KEY = str(os.getenv('eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNmIzNTZkNzBhODAwMWJjN2EyZmIwY2I1YTE4OWUzNCIsInN1YiI6IjY1NGRiMWI1MWFjMjkyN2IzMzg5ZjMzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lP1ygCFHtWs1lpM4YRyumg54HMNp2AnMgeDrrBpamdg'))

def get_movie_datas():
    total_data = []

    # 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 501):
        request_url = f"<https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}>"
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('release_date', ''):
                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'released_date': movie['release_date'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids']
                    # 'popularity': movie['popularity'],
                    # 'vote_avg': movie['vote_average'],
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("movie_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\\t", ensure_ascii=False)

get_movie_datas()


    
# 장르 데이터 가져오기
genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=ko-KR"
genre_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}
genre_res = requests.get(genre_url, headers=genre_headers).json()
genres = genre_res["genres"]

