from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    have_review_movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='movie_review', null=True, blank=True)
    # 게시글을 작성한 사용자
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews')
    like_count = models.IntegerField(null=True )