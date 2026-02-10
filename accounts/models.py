from django.contrib.auth.models import AbstractUser
from django.db import models

class ArtHubUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email Address"
    )

    professional_artist = models.BooleanField(
        default=False,
    )

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip().capitalize()
        if self.last_name:
            self.last_name = self.last_name.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username