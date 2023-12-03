from rest_framework import serializers
from ..models import *
# from django.contrib.auth import get_user_model


# 전체 영화 조회용 Serializer (줄거리 X, 투표한 사람 수 X)
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 영화 id, 제목, 포스터 주소, 개봉일, 장르
        fields = (
            'id', 'title', 'overview', 'poster_path', 'released_date', 'genre', 'popularity', 'vote_count', 'vote_average',
            )
        

# 단일 영화 조회용 Serializer 
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 영화 id, 제목, 줄거리, 포스터 주소, 개봉일, 장르, 투표 유저
        fields = (
            'id', 'title', 'overview', 'poster_path', 'released_date', 'genre',
            'rates_users',)


# 영화 작성 Serializer
class MovieCreateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Movie
        # 영화 id, 제목, 개봉일, 평점, 포스터 주소, 줄거리
        fields = ('id', 'title', 'released_date', 'poster_path', 'overview', 'creater') 

class MovieUpdateSerializer(serializers.ModelSerializer):   

    class GenreSerializer(serializers.ModelSerializer): 
        class Meta:
            model = Genre
            fields = '__all__'
    
    genre_check = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 제목, 장르(id, name), 개봉일, 포스터 주소, 개요
        fields = ('id', 'title', 'genre_check', 'release_date', 'poster_path', 'overview')
        read_only_fields = ('id',)



# 영화 데이터 받아오기용 Serializer
class MovieGenreSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Genre    
        fields = '__all__'  



# 영화 데이터 받아오기용 Serializer
class MovieDataSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all(), required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'poster_path', 'released_date', 'genre', 'popularity', 'vote_count', 'vote_average',)

    def create(self, validated_data):
        genres_data = validated_data.pop('genre', [])  # genre 데이터 추출
        movie = Movie.objects.create(**validated_data)  # Movie 객체 생성
        for genre_data in genres_data:
            genre = Genre.objects.get(pk=genre_data.pk)  # Genre 객체 가져오기
            movie.genre.add(genre)  # Movie와 Genre의 ManyToMany 관계 설정

        return movie
    

# 영화 장르 드롭다운 Serializer
class MovieGenreSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
 