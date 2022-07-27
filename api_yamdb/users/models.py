from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Administrator"),
    ]

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
