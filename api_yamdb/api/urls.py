from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegisterUserViewSet

router = DefaultRouter()
router.register("auth/signup", RegisterUserViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
