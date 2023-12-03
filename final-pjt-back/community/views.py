# Create your views here.
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import *
from .serializers.review import *
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


# 전체 리뷰 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.annotate(
                cnt_like=Count('likers', distinct=True),
            ).order_by('-pk')
        serializer = ReviewListSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


# 리뷰 정렬(최신순, 좋아요 순)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def review_sort(request, sort_num):
    reviews = Review.objects.annotate(
                cnt_like = Count('likers', distinct=True), # 좋아요 수
            )
    if sort_num == 1: # 최신순
        sort_reviews = reviews.order_by('-created_at')
    elif sort_num == 2: # 좋아요 순
        sort_reviews = reviews.order_by('-cnt_like')
        
    serializer = ReviewListSerializer(sort_reviews, many=True, context={'request': request})
    return Response(serializer.data)


# 영화 리뷰 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_C(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    serializer = ReviewCreateSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        # 객체 생성 시 reviewer와 review_movie 필드는 제외하고 생성
        review = Review.objects.create(
            title=serializer.validated_data['title'], 
            content=serializer.validated_data['content'], 
            user=request.user,
            reviewer=request.user,
            have_review_movie=movie,
        )
        
        # 생성된 review 객체를 다시 직렬화
        serializer = ReviewSerializer(review)
        
        # 리뷰의 좋아요와 댓글 수를 업데이트할 필요가 있다면 해당 로직 추가
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 특정 영화 리뷰 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_R(request, movie_id):
    reviews = Review.objects.filter(have_review_movie_id=movie_id).annotate(
        cnt_like=Count('likers', distinct=True), 
    ) 
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# 단일 리뷰 수정, 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_UD(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'error': 'Review does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        data = {
        'delete': f'{review_id}번 리뷰가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)



# 리뷰 좋아요 등록 및 해제
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def review_like(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    user = request.user

    if review.likers.filter(pk=user.pk).exists():
        review.likers.remove(user)
    else:
        review.likers.add(user)
    
    # 좋아요 개수를 갱신
    review.like_count = review.likers.count()
    # 좋아요를 누른 사람의 리스트 갱신
    likers_list = [user.id for user in review.likers.all()]

    review.save()

    serializer = ReviewLikeSerializer(review)

    like_status = {
        'id' : serializer.data.get('id'),
        'count' : review.like_count,
        'like_list' : likers_list,
    }
    return JsonResponse(like_status)
