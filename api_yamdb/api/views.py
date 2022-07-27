from django.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from users.models import User

from .permissions import RegisterUser
from .serializers import UserSerializer


class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (RegisterUser,)

    def perform_create(self, serializer):
        """Check username."""
        username = serializer.validated_data.get("username")
        if username.lower() in settings.PROHIBITED_USER_NAMES:
            raise ParseError(detail=f"Username '{username}' is not allowed")
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )
