from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, GenresViewSet, TitleViewSet
from api.views import (
    ManageUsersViewSet,
    PersonalProfileView,
    RegisterUserViewSet,
    RequestJWTView,)

app_name = "api"

router = DefaultRouter()
router.register("auth/signup", RegisterUserViewSet)
router.register("users", ManageUsersViewSet)
router.register("categories", CategoriesViewSet, basename="categories")
router.register("genres", GenresViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")

urlpatterns = [
    path(
        "v1/users/me/", PersonalProfileView.as_view(),name="personal-profile"
    ),
    path(
        "v1/auth/token/", RequestJWTView.as_view(), name="request-jwt"
    ),
    path("v1/", include(router.urls)),
]
