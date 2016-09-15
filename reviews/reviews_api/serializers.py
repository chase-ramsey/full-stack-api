from rest_framework import serializers
from django.contrib.auth.models import User
from reviews_api.models import Media, Review, Tag, ReviewTag, List, ListReview

class MediaSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Media
    fields = ('id', 'url', 'media_type', 'title', 'creator', 'yearReleased')

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Review
    fields = ('id', 'url', 'media', 'user', 'full_text', 'edited')

class TagSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Tag
    fields = ('id', 'url', 'word')

class ReviewTagSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = ReviewTag
    fields = ('id', 'url', 'review', 'tag')

class ListSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = List
    fields = ('id', 'user')

class ListReviewSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = ListReview
    fields = ('id', 'review')

class UserSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'url', 'username')
