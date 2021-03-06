from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings

class MediaChoice(models.Model):
  choice_name = models.CharField(max_length=15)

  def __str__(self):
    return self.choice_name


class Media(models.Model):
  title = models.CharField(max_length=100)
  creator = models.CharField(max_length=100)
  year_released = models.IntegerField()
  media_choice = models.ForeignKey(MediaChoice, on_delete=models.CASCADE, related_name="media")

  def __str__(self):
    return self.title


class Review(models.Model):
  media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='reviews')
  owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews')
  full_text = models.TextField()
  watson_report = models.TextField()
  edited = models.DateTimeField(auto_now_add=True)
  image_url = models.CharField(max_length=150, default='https://firebasestorage.googleapis.com/v0/b/full-stack-images.appspot.com/o/file-media.svg?alt=media&token=8bb8a118-f9b4-422b-a8fc-9974eb8094de')
  featured = models.BooleanField(default=False)

  def __str__(self):
    return self.media.title


class Tag(models.Model):
  word = models.CharField(max_length=50)

  def __str__(self):
    return self.word


class ReviewTag(models.Model):
  review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_tags')
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='review_tags')


class List(models.Model):
  owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='lists')
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class ListReview(models.Model):
  list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list_reviews')
  review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='list_reviews')


class UserImage(models.Model):
  owner = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='image')
  image_url = models.CharField(max_length=150, default='https://firebasestorage.googleapis.com/v0/b/full-stack-images.appspot.com/o/person.svg?alt=media&token=51e701f8-817f-4b7e-a79e-353e7561ec36')

class UserFeatured(models.Model):
  owner = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='featured')
  featured = models.BooleanField(default=False)

  def __str__(self):
    return self.owner.username
