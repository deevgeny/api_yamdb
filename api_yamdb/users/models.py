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
