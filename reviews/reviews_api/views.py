from reviews_api.models import *
from django.contrib.auth import logout, login, authenticate
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
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import reviews_api.permissions

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
        'userimages': reverse('userimages', request=request),
        'featuredusers': reverse('featuredusers', request=request),
        'featuredreviews': reverse('featuredreviews', request=request),
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
  lookup_field = 'choice_name'

class MediaList(ListView):
  model = Media
  queryset = Media.objects.all()
  serializer_class = MediaSerializer

  def post(self, request, *args, **kwargs):
    req_body = json.loads(request.body.decode())
    mc = MediaChoice.objects.get(choice_name=req_body['media_choice'])

    media_inst = Media.objects.create(
      media_choice=mc,
      title=req_body['title'],
      creator=req_body['creator'],
      year_released=req_body['year_released'],
    )
    media_inst.save()

    media_res = MediaSerializer(media_inst, context={'request': request})
    return Response(media_res.data)

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

  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        reviews_api.permissions.IsOwnerOrReadOnly)

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    report = review_report.make_call(request.data['full_text'])
    review = request.data

    rev_inst = Review.objects.create(
      media = Media.objects.get(pk=int(review['media'].split('/')[-2])),
      owner = self.request.user,
      full_text = review['full_text'],
      watson_report = report,
    )
    rev_inst.save()

    try:
      rev_inst.image_url = review['image_url']
    except KeyError:
      pass

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

  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        reviews_api.permissions.IsOwnerOrReadOnly)

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    report = review_report.make_call(request.data['full_text'])
    request.data['watson_report'] = report
    res = self.update(request, *args, **kwargs)

    tags.create_review_tags(data=request.data, id=kwargs['pk'], update=True)

    return res

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

  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        reviews_api.permissions.IsOwnerOrReadOnly)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class ListDetail(DetailView):
  model = List
  queryset = List.objects.all()
  serializer_class = ListSerializer

  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        reviews_api.permissions.IsOwnerOrReadOnly)



class ListReviewList(ListView):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer

  def post(self, request, *args, **kwargs):
    req_body = json.loads(request.body.decode())
    review = Review.objects.get(id=req_body['review'])
    list_id = List.objects.get(id=req_body['list_id'])

    lr_inst = ListReview.objects.create(
      review = review,
      list_id = list_id
    )

    lr_inst.save()

    lr_res = ListReviewSerializer(lr_inst, context={'request': request})
    return Response(lr_res.data)

class ListReviewDetail(DetailView):
  model = ListReview
  queryset = ListReview.objects.all()
  serializer_class = ListReviewSerializer

class ListReviewMatch(ListView):
  model = ListReview
  serializer_class = ListReviewSerializer

  def get(self, request, *args, **kwargs):
    self.queryset = ListReview.objects.filter(list_id=kwargs['list_id'])
    return self.list(request, *args, **kwargs)



class UserList(ListView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def post(self, request, *args, **kwargs):
    new_user = self.create(request, *args, **kwargs)
    uf = UserFeatured.objects.create(owner=User.objects.get(pk=int(new_user.data['id'])))
    uf.save()
    if request.data['image_url'] != '':
      ui = UserImage.objects.create(owner=User.objects.get(pk=int(new_user.data['id'])), image_url=request.data['image_url'])
      ui.save()
    else:
      ui = UserImage.objects.create(owner=User.objects.get(pk=int(new_user.data['id'])))
      ui.save()

    return new_user

class UserDetail(DetailView):
  queryset = User.objects.all()
  serializer_class = UserSerializer



class UserImageList(ListView):
  model = UserImage
  queryset = UserImage.objects.all()
  serializer_class = UserImageSerializer

class UserImageDetail(DetailView):
  model = UserImage
  queryset = UserImage.objects.all()
  serializer_class = UserImageSerializer

class UserFeaturedList(ListView):
  model = UserFeatured
  queryset = UserFeatured.objects.all()
  serializer_class = UserFeaturedSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)



class FeaturedUserList(ListView):
  model = User
  queryset = User.objects.filter(featured=True)
  serializer_class = UserSerializer

class FeaturedReviewList(ListView):
  model = Review
  queryset = Review.objects.filter(featured=True)
  serializer_class = ReviewSerializer

@csrf_exempt
def login_user(request):
    req_body = json.loads(request.body.decode())

    auth = authenticate(
            username=req_body['username'],
            password=req_body['password']
            )

    success = True
    if auth is not None:
        login(request=request, user=auth)
        uid = auth.id
        data = json.dumps({"success":success, "uid": uid})
    else:
        success = False
        data = json.dumps({"success":success})

    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create(
      first_name=req_body['first_name'],
      last_name=req_body['last_name'],
      email=req_body['email'],
      username=req_body['username'],
    )

    new_user.set_password(req_body['password']);

    new_user.save()

    uf = UserFeatured.objects.create(owner=new_user)
    try:
      ui = UserImage.objects.create(owner=new_user, image_url=req_body['image_url'])
    except KeyError:
      ui = UserImage.objects.create(owner=new_user)

    data = json.dumps({"success":True})
    return HttpResponse(data, content_type='application/json')
