from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

class ArtHubUser(AbstractUser):
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )

    professional_artist = models.BooleanField(
        default=False,
        help_text="Check if you create art professionally."
    )

    def __str__(self):
        return self.username