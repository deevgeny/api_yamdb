from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Administrator"),
    ]

    email = models.EmailField(_("email address"), unique=True)

    role = models.CharField(
        "User role",
        choices=ROLE_CHOICES,
        default=USER,
        max_length=8,
        blank=True,
    )
    bio = models.TextField(
        "Bio",
        blank=True,
    )
    confirmation_code = models.CharField(max_length=24, blank=True)

    def save(self, *args, **kwargs):
        """Update is_staff for admin users."""
        if self.role == User.ADMIN:
            self.is_staff = True
        if self.is_superuser:
            self.role = User.ADMIN
        super(User, self).save(*args, **kwargs)

    #  тесты Жанров, Категории, и произведения не проходят без этого
    #  такая ошибка
    #  def has_permission(self, request, view):
    #      return (request.method in permissions.SAFE_METHODS
    #              or request.user.is_authenticated and request.user.is_admin)
    #      AttributeError: 'User' object has no attribute 'is_admin'
    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN
