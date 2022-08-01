from api.filters import TitleFilter
from api.pagination import CustomPagination
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.tokens import confirmation_code

from .permissions import (
    AccessPersonalProfileData,
    AdminUserOnly,
    AdminUserOrReadOnly,
    AllowPostForAnonymousUser,
    ReviewCommentPermission,
)
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    CreateTitleSerializer,
    GenresSerializer,
    RegisterUserSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)

User = get_user_model()


# Helper functions
def check_required_fields(request, field_names):
    """Check required fields and return errors or None."""
    errors = {}
    for field_name in field_names:
        if not request.data.get(field_name):
            errors[field_name] = ["This field is required."]
    if len(errors) > 0:
        return errors


class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """New user registration view."""

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowPostForAnonymousUser,)

    def perform_create(self, serializer):
        """Check username, create confirmation code, save and send email."""
        # Check username
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        if username.lower() in settings.PROHIBITED_USER_NAMES:
            raise ParseError(detail=f"Username '{username}' is not allowed")
        # Create confirmation code and save user
        user = User(username=username)
        token = confirmation_code.make_token(user)
        serializer.save(confirmation_code=token)
        # Send email with confirmation code
        send_mail(
            subject=settings.CONFIRMATION_SUBJECT,
            message=settings.CONFIRMATION_MESSAGE.format(token),
            from_email=settings.SIGNUP_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        """Override response status to 200_OK."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class RequestJWTView(views.APIView):
    """Request JWT token view."""

    permission_classes = (AllowPostForAnonymousUser,)

    def post(self, request):
        # Check required fields
        required_fields = ["username", "confirmation_code"]
        errors = check_required_fields(request, required_fields)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        # Get user from db and check confirmation code
        user = get_object_or_404(User, username=request.data.get("username"))
        if user.confirmation_code != request.data.get("confirmation_code"):
            return Response(
                {"confirmation_code": ["Does not match."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({"token": str(refresh.access_token)})


class ManageUsersViewSet(viewsets.ModelViewSet):
    """Manage users view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (AdminUserOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("username",)
    ordering = ("username",)

    def perform_create(self, serializer):
        """Check username."""
        username = serializer.validated_data.get("username")
        if username.lower() in settings.PROHIBITED_USER_NAMES:
            raise ParseError(detail=f"Username '{username}' is not allowed")
        serializer.save()


class PersonalProfileView(views.APIView):
    """Read and edit personal profile data view."""

    permission_classes = (AccessPersonalProfileData,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        # Do not allow user to change his role
        data = request.data.dict()
        if request.data.get("role"):
            data["role"] = user.role
        serializer = UserSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = CustomPagination
    permission_classes = (AdminUserOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering = ("name",)


class GenresViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Genre viewset."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    pagination_class = CustomPagination
    permission_classes = (AdminUserOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset."""

    queryset = Title.objects.all()
    permission_classes = (AdminUserOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering = ("name",)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleSerializer
        return CreateTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        username = self.request.user.username
        user = get_object_or_404(User, username=username)
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(title=title, author=user).exists():
            raise ParseError(
                detail={"Integrity error": "This review already exists"}
            )
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        username = self.request.user.username
        user = get_object_or_404(User, username=username)
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=user, review=review)
