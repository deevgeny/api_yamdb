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
        name="User role",
        max_length=8,
        blank=False,
        default=USER,
        choices=ROLE_CHOICES,
    )
