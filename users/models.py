from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        HOST = "host", "Host"
        GUEST = "guest", "Guest"

    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    # ------------------------
    # Authentication settings
    # ------------------------
    USERNAME_FIELD = "username" 
    REQUIRED_FIELDS = ["email"]
    def __str__(self):
        return f"{self.username} ({self.role})"

    # ------------------------
    # Role helpers
    # ------------------------
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_host(self):
        return self.role == self.Role.HOST

    def is_guest(self):
        return self.role == self.Role.GUEST
