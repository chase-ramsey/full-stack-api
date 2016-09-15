from django.db import models
from django.utils import timezone

class Media(models.Model):
  ALBUM = 'AB'
  BOOK = 'BK'
  VIDEOGAME = 'VG'
  MOVIE = 'MV'
  SHOW = 'TV'
  MEDIA_CHOICES = (
    (ALBUM, 'Album'),
    (BOOK, 'Book'),
    (VIDEOGAME, 'Videogame'),
    (MOVIE, 'Movie'),
    (SHOW, 'TV Show'),
  )
  media_type = models.CharField(max_length=2, choices=MEDIA_CHOICES)
  title = models.CharField(max_length=100)
  creator = models.CharField(max_length=100)
  yearReleased = models.IntegerField()

  def __str__(self):
    return self.title


class Review(models.Model):
  media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='reviews')
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user')
  full_text = models.TextField()
  watson_report = models.TextField()
  edited = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
  word = models.CharField(max_length=50)

  def __str__(self):
    return self.word


class ReviewTag(models.Model):
  review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_tags')
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='review_tags')


class List(models.Model):
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='lists')


class ListReview(models.Model):
  list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list_reviews')
  review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='list_reviews')
