from django.urls import path
from . import views


urlpatterns = [
    path('', views.movies_index), # 전체 영화 조회(메인페이지)
    path('<int:pk>/', views.movie_detail), # 단일 영화 조회
    path('create/', views.movie_create), # 영화 작성 (관리자가 할 수 있게?)
    path('<int:pk>/edit/', views.movie_update), # 영화 수정
    path('<int:pk>/delete/', views.movie_delete), # 영화 삭제
    path('genredata/', views.get_genre_datas), # 영화 데이터 받아오기(fixture용 주소)
    path('data/', views.get_movie_datas), # 영화 데이터 받아오기(fixture용 주소)
    path('show/<int:sort_num>/', views.show_movies_algorithm), # 영화 추천 알고리즘
    path('genre/<int:genre_id>/', views.genre_dropdown), # 영화 추천 알고리즘
]
