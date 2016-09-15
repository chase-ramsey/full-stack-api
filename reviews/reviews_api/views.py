from reviews_api.models import Media, Review, Tag, ReviewTag, List, ListReview
from reviews_api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
import reviews_api.review_report

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'reviews': reverse('reviews', request=request),
        'media': reverse('media', request=request),
    })


class MediaList(viewsets.ModelViewSet):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer

class MediaDetail(viewsets.ModelViewSet):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer
  lookup_field = 'title'



class ReviewList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  model = Review
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    report = review_report.make_call(request.data.full_text)
    review = request.data
    review.watson_report = report

    rev_inst = Review.objects.create(
      media = Media.objects.get(pk=review.media),
      user = User.objects.get(pk=review.user),
      full_text = review.full_text,
      watson_report = review.watson_report
    )
    rev_inst.save()

    tags.create_review_tags(rev_inst)

    return Response(rev_inst)

class ReviewDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    report = review_report.make_call(request.data.full_text)
    review = request.data
    review.watson_report = report

    rev_inst = Review.objects.create(
      media = Media.objects.get(pk=review.media),
      user = User.objects.get(pk=review.user),
      full_text = review.full_text,
      watson_report = review.watson_report
    )
    rev_inst.save()

    tags.create_review_tags(rev_inst, update=True)

    return self.update(review)

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
