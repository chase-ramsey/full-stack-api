from rest_framework import routers
from django.conf.urls import url, include
from reviews_api.views import *

router = routers.DefaultRouter()
router.register(r'media', MediaList)
router.register(r'review-tags', ReviewTagList)
router.register(r'lists', ListList)
router.register(r'list-reviews', ListReviewList)
router.register(r'users', UserList)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^reviews', ReviewList.as_view()),
    url(r'^reviews/(?P<review_id>[0-9]*)/$', ReviewDetail.as_view()),
]
