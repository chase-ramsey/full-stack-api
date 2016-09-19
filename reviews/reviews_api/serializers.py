from rest_framework import serializers
from django.contrib.auth.models import User
from reviews_api.models import *

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
  owner = serializers.ReadOnlyField(source='owner.username')
  review_tags = ReviewTagSerializer(many=True, read_only=True)

  class Meta:
    model = Review
    fields = ('id', 'url', 'media', 'owner', 'full_text', 'watson_report', 'edited', 'image', 'review_tags', 'featured')
    extra_kwargs = {'watson_report': {'read_only': True}}

class ListSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = List
    fields = ('id', 'owner', 'name')

class ListReviewSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = ListReview
    fields = ('id', 'review', 'list_id')

class UserFeaturedSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = UserFeatured
    fields = ('id', 'owner', 'featured')


class UserImageSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = UserImage
    fields = ('id', 'url', 'image', 'owner')

class UserSerializer(serializers.HyperlinkedModelSerializer):
  reviews = ReviewSerializer(many=True, read_only=True)
  lists = ListSerializer(many=True, read_only=True)
  image = UserImageSerializer(read_only=True)
  featured = UserFeaturedSerializer(read_only=True)

  class Meta:
    model = User
    fields = ('id', 'url', 'username', 'reviews', 'lists', 'image', 'featured')
