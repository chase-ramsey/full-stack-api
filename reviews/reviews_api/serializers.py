from rest_framework import serializers
from django.contrib.auth.models import User
from reviews_api.models import MediaChoice, Media, Review, Tag, ReviewTag, List, ListReview

class MediaChoiceSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = MediaChoice
    fields = ('id', 'url', 'choice_name')

class MediaSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Media
    fields = ('id', 'url', 'media_choice', 'title', 'creator', 'year_released')

class TagSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Tag
    fields = ('id', 'url', 'word')

class ReviewTagSerializer(serializers.HyperlinkedModelSerializer):

  tag = TagSerializer(read_only=True)

  class Meta:
    model = ReviewTag
    fields = ('id', 'url', 'review', 'tag')
    extra_kwargs = {'review': {'read_only': True},
                    'tag': {'read_only': True}}

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

  review_tags = ReviewTagSerializer(many=True, read_only=True)

  class Meta:
    model = Review
    fields = ('id', 'url', 'media', 'user', 'full_text', 'watson_report', 'edited', 'review_tags')
    extra_kwargs = {'watson_report': {'read_only': True}}

class ListSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = List
    fields = ('id', 'user')

class ListReviewSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = ListReview
    fields = ('id', 'review', 'list_id')
    extra_kwargs = {'review': {'read_only': True},
                    'list_id': {'read_only': True}}

class UserSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'url', 'username')
