from django.db import models
from django.utils import timezone

class Media(models.Model):
  media_type = models.ChoiceField('album', 'book', 'game', 'movie', 'show')
  title = models.CharField(max_length=100)
  creator = models.CharField(max_length=100)
  yearReleased = models.IntegerField()

  def __str__(self):
    return self.title


class Review(models.Model):
  media = models.ForeignKey(Media, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  full_text = models.TextField()
  processed_text = models.TextField()


class Tag(models.Model):
  word = models.CharField(max_length=50)

  def __str__(self):
    return self.word


class ReviewTag(models.Model):
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class List(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)


class ListReview(models.Model):
  list = models.ForeignKey(List, on_delete=models.CASCADE)
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
