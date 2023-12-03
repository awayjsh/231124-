from django.urls import path
from . import views

urlpatterns = [
    # review
    path('', views.review_list), # 전체 게시글 조회
    path('<int:sort_num>/sort/', views.review_sort), # 게시글 정렬(최신순, 좋아요, 댓글 많은 순)
    path('<int:movie_id>/review/', views.review_C),# 영화 리뷰 생성
    path('<int:movie_id>/', views.review_R), # 특정 영화 리뷰 조회
    path('<int:review_id>/ud/', views.review_UD), # 단일 리뷰 수정, 삭제
    path('<int:review_id>/like/', views.review_like), # 리뷰 좋아요 등록 및 해제
]