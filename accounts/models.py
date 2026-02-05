from django.contrib.auth.models import AbstractUser
from django.db import models

class ArtHubUser(AbstractUser):
    professional_artist = models.BooleanField(
        default=False,
        help_text="Check if you create art professionally."
    )

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip().capitalize()
        if self.last_name:
            self.last_name = self.last_name.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username