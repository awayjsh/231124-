from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Movie, Genre
from .serializers.movie import *
import requests


# TMDB API 키
TMDB_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNmIzNTZkNzBhODAwMWJjN2EyZmIwY2I1YTE4OWUzNCIsInN1YiI6IjY1NGRiMWI1MWFjMjkyN2IzMzg5ZjMzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lP1ygCFHtWs1lpM4YRyumg54HMNp2AnMgeDrrBpamdg'

# Create your views here.
# 전체 영화 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movies_index(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 단일 영화 디테일 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 단일 영화 만들기
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_create(request):
    serializer = MovieCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 작성자 입력 변수 주의 !!
        serializer.save(creater = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# # 단일 영화 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'PUT':
        if request.user == movie.creater:
            serializer = MovieUpdateSerializer(movie, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


# 단일 영화 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'DELETE':
        # if request.user == movie.creater: # # 구현하려다가 뺌
        movie.delete()
        data = {
            'delete': f'{pk}번 영화가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_genre_datas(request):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNmIzNTZkNzBhODAwMWJjN2EyZmIwY2I1YTE4OWUzNCIsInN1YiI6IjY1NGRiMWI1MWFjMjkyN2IzMzg5ZjMzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lP1ygCFHtWs1lpM4YRyumg54HMNp2AnMgeDrrBpamdg"
    }

    res = requests.get(url, headers=headers).json()
    print('get_genre_datas')
    print(res)
    # 응답 데이터를 직렬화하여 저장
    for genre in res['genres']:
        save_data = {
            'id': genre['id'],
            'name': genre['name']
        }
        try:
            genre_instance = Genre.objects.get(id=save_data['id'])
            serializer = MovieGenreSerializer(genre_instance, data=save_data)
        except Genre.DoesNotExist:
            serializer = MovieGenreSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return JsonResponse({'msg': 'hi'})



# 영화 데이터 받아오기
def get_movie_datas(request):
    for i in range(1, 4):
        url = f"https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"
        }
        res = requests.get(url, headers=headers).json()

        for result in res['results']:
            fields = {
                'id': result['id'],
                'title': result['title'],
                'overview': result['overview'],
                'poster_path': result['poster_path'],
                'released_date': result['release_date'],
                'popularity': result['popularity'],
                'vote_count': result['vote_count'],
                'vote_average': result['vote_average'],
                'genre': result['genre_ids']  # 장르 ID 리스트를 전달
            }
            try:
                movie = Movie.objects.get(id=fields['id'])
                serializer = MovieDataSerializer(movie, data=fields)
            except Movie.DoesNotExist:
                serializer = MovieDataSerializer(data=fields)

            if serializer.is_valid():
                serializer.save()
            else:
                print('**errors**')
                print(serializer.errors)    
    return JsonResponse({"message": "hello world"})



# ================================= #
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def show_movies_algorithm(request, sort_num):
    if sort_num == 1: # 관람객 수
        movies = Movie.objects.order_by('-popularity')[:10]
    elif sort_num == 2: # 투표 수
        movies = Movie.objects.order_by('-vote_count')[:10]
    elif sort_num == 3: # 평점 수
        movies = Movie.objects.order_by('-vote_average')[:10]
        
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def genre_dropdown(request, genre_id):
    movies = Movie.objects.filter(genre__id=genre_id)
    serializer = MovieGenreSortSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)