from rest_framework import routers
from django.conf.urls import url, include
from reviews_api import views

router = routers.DefaultRouter()
router.register(r'media', views.MediaList)
router.register(r'reviews', views.ReviewList)
router.register(r'review-tags', views.ReviewTagList)
router.register(r'lists', views.ListList)
router.register(r'list-reviews', views.ListReviewList)
router.register(r'users', views.UserList)

urlpatterns = [
    url(r'^', include(router.urls)),
]
