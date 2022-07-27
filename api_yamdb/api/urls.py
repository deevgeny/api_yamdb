from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminRegisterUserViewSet, RegisterUserViewSet, RequestJWT

router = DefaultRouter()
router.register("auth/signup", RegisterUserViewSet)
router.register("users", AdminRegisterUserViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/token/", RequestJWT.as_view()),
]
