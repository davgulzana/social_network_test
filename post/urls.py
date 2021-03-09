from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, LikesAnalytics

router = DefaultRouter()
router.register("", PostViewSet)


urlpatterns = [
    path("analytics/", LikesAnalytics.as_view()),
    path("", include(router.urls)),
]
