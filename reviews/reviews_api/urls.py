from django.conf.urls import url, include
from reviews_api.views import *

urlpatterns = [
  url(r'^reviews/$', ReviewList.as_view(), name='reviews'),
  url(r'^reviews/(?P<pk>[0-9]*)/$', ReviewDetail.as_view(), name="review-detail"),
  url(r'^reviews/featured/$', FeaturedReviewList.as_view(), name='featuredreviews'),
  url(r'^mediachoices/$', MediaChoiceList.as_view(), name='mediachoices'),
  url(r'^mediachoices/(?P<pk>[0-9]*)/$', MediaChoiceDetail.as_view(), name="mediachoice-detail"),
  url(r'^media/$', MediaList.as_view(), name='media'),
  url(r'^media/(?P<pk>[0-9]*)/$', MediaDetail.as_view(), name="media-detail"),
  url(r'^tags/$', TagList.as_view(), name='tags'),
  url(r'^tags/(?P<pk>[0-9]*)/$', TagDetail.as_view(), name="tag-detail"),
  url(r'^reviewtags/$', ReviewTagList.as_view(), name='reviewtags'),
  url(r'^reviewtags/(?P<pk>[0-9]*)/$', ReviewTagDetail.as_view(), name="reviewtag-detail"),
  url(r'^lists/$', ListList.as_view(), name='lists'),
  url(r'^lists/(?P<pk>[0-9]*)/$', ListDetail.as_view(), name="list-detail"),
  url(r'^listreviews/$', ListReviewList.as_view(), name='listreviews'),
  url(r'^listreviews/(?P<pk>[0-9]*)/$', ListReviewDetail.as_view(), name="listreview-detail"),
  url(r'^listreviews/list/(?P<list_id>[0-9]*)/$', ListReviewMatch.as_view(), name="listreview-match"),
  url(r'^users/$', UserList.as_view(), name='users'),
  url(r'^users/(?P<pk>[0-9]*)/$', UserDetail.as_view(), name="user-detail"),
  url(r'^users/featured/$', FeaturedUserList.as_view(), name='featuredusers'),
  url(r'^userimages/$', UserImageList.as_view(), name='userimages'),
  url(r'^userimages/(?P<pk>[0-9]*)/$', UserImageDetail.as_view(), name="userimage-detail"),
  url(r'^login/$', login_user, name='login'),
  url(r'^$', api_root),
]
