from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.tokens import confirmation_code

from .permissions import AdminRegisterUser, AllowPostMethod
from .serializers import UserSerializer

User = get_user_model()


class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowPostMethod,)

    def perform_create(self, serializer):
        """Check username and create token."""
        # Check username
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        if username.lower() in settings.PROHIBITED_USER_NAMES:
            raise ParseError(detail=f"Username '{username}' is not allowed")
        # Create token and save user
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
        """Change response status."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class AdminRegisterUserViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminRegisterUser,)

    def perform_create(self, serializer):
        """Check username."""
        username = serializer.validated_data.get("username")
        if username.lower() in settings.PROHIBITED_USER_NAMES:
            raise ParseError(detail=f"Username '{username}' is not allowed")
        serializer.save()


class RequestJWT(views.APIView):
    """Request JWT token after registration."""

    permission_classes = (AllowPostMethod,)

    def post(self, request):
        # Check request fields and response errors
        errors = {}
        if not request.data.get("username"):
            errors["username"] = ["This field is required."]
        if not request.data.get("confirmation_code"):
            errors["confirmation_code"] = ["This field is required."]
        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        # Get user from db, check confirmation code and response errors
        user = get_object_or_404(User, username=request.data.get("username"))
        if user.confirmation_code != request.data.get("confirmation_code"):
            return Response(
                {"confirmation_code": ["Does not match."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({"token": str(refresh.access_token)})
