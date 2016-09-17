from reviews_api.models import MediaChoice, Media, Review, Tag, ReviewTag, List, ListReview
from reviews_api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from reviews_api import review_report
from reviews_api import tags

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'reviews': reverse('reviews', request=request),
        'media': reverse('media', request=request),
        'users': reverse('users', request=request),
        'mediachoices': reverse('mediachoices', request=request),
        'tags': reverse('tags', request=request),
        'reviewtags': reverse('reviewtags', request=request),
        'lists': reverse('lists', request=request),
        'listreviews': reverse('listreviews', request=request),
        'users': reverse('users', request=request),
    })

class ListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MediaChoiceList(ListView):
  model = MediaChoice
  queryset = MediaChoice.objects.all()
  serializer_class = MediaChoiceSerializer

class MediaChoiceDetail(DetailView):
  model = MediaChoice
  queryset = MediaChoice.objects.all()
  serializer_class = MediaChoiceSerializer

class MediaList(ListView):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer

class MediaDetail(DetailView):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer


class ReviewList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  model = Review
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    report = review_report.make_call(request.data['full_text'])
    review = request.data

    rev_inst = Review.objects.create(
      media = Media.objects.get(pk=int(review['media'].split('/')[-2])),
      user = User.objects.get(pk=int(review['user'].split('/')[-2])),
      full_text = review['full_text'],
      watson_report = report
    )
    rev_inst.save()

    tags.create_review_tags(review=rev_inst)

    review_res = ReviewSerializer(rev_inst, context={'request': request})
    return Response(review_res.data)

class ReviewDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    report = review_report.make_call(request.data['full_text'])
    request.data['watson_report'] = report
    res = self.update(request, *args, **kwargs)

    tags.create_review_tags(data=request.data, id=kwargs['pk'], update=True)

    update_res = ReviewSerializer(res)
    return update_res

  def delete(self, request, *args, **kwargs):
    delete_res = self.destroy(request, *args, **kwargs)
    tags.clean_up_tags()
    return delete_res



class TagList(ListView):
  model = Tag
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class TagDetail(DetailView):
  model = Tag
  queryset = Tag.objects.all()
  serializer_class = TagSerializer



class ReviewTagList(ListView):
  model = ReviewTag
  queryset = ReviewTag.objects.all()
  serializer_class = ReviewTagSerializer

class ReviewTagDetail(DetailView):
  model = ReviewTag
  queryset = ReviewTag.objects.all()
  serializer_class = ReviewTagSerializer



class ListList(ListView):
  model = List
  queryset = List.objects.all()
  serializer_class = ListSerializer

class ListDetail(DetailView):
  model = List
  queryset = List.objects.all()
  serializer_class = ListSerializer



class ListReviewList(ListView):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer

class ListReviewDetail(DetailView):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer



class UserList(ListView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(DetailView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
