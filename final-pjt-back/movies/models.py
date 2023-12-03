from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=50)
    released_date = models.CharField(max_length=50)
    popularity = models.FloatField(null=True, blank=True) # 관객 수
    vote_count = models.IntegerField(null=True, blank=True) # 투표 수
    vote_average = models.FloatField(null=True, blank=True) # 평점
    # 평점 준 유저
    rates_users = models.ManyToManyField('accounts.User', related_name='user_rated_movie', through='Rate')
    genre = models.ManyToManyField(Genre, related_name='genre_movies', blank=True) # id로 저장
    
    # 홈페이지에 영화 글 올리는 사람
    creater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_movies', null=True, blank=True)


# 중계 테이블
class Rate(models.Model):
    rate_user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='user_rated'
        )
    rate_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 사용자가 준 평점 : 추가 필드
    rate_score = models.FloatField()