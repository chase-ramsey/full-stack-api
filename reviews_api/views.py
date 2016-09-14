from reviews_api.models import Media, Review, Tag, ReviewTag, List, ReviewList
from reviews_api.serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics



class MediaList(viewsets.ModelViewSet):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer

class MediaDetail(viewsets.ModelViewSet):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer
  lookup_field = 'title'



class ReviewList(viewsets.ModelViewSet):
  model = Review
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

class ReviewDetail(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView)
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def create(self, request, *args, **kwargs):
    pass

  def put(self, request, *args, **kwargs):
    pass

  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)



class TagList(viewsets.ModelViewSet):
  model = Tag
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class TagDetail(viewsets.ModelViewSet):
  model = Tag
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'word'



class ReviewTagList(viewsets.ModelViewSet):
  model = ReviewTag
  queryset = ReviewTag.objects.all()
  serializer_class = ReviewTagSerializer

class ReviewTagDetail(viewsets.ModelViewSet):
  model = ReviewTag
  queryset = ReviewTag.objects.all()
  serializer_class = ReviewTagSerializer



class ListList(viewsets.ModelViewSet):
  model = List
  queryset = List.objects.all()
  serializer_class = ListSerializer

class ListDetail(viewsets.ModelViewSet):
  model = List
  queryset = List.objects.all()
  serializer_class = ListSerializer



class ListReviewList(viewsets.ModelViewSet):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer

class ListReviewDetail(viewsets.ModelViewSet):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer



class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
