from django.contrib.auth.models import AbstractUser
from django.db import models


class ArtHubUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email Address"
    )

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip().capitalize()
        if self.last_name:
            self.last_name = self.last_name.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    professional_artist = models.BooleanField(
        default=False,
    )

    avatar = models.ImageField(
        upload_to='user-avatars/',
        blank=True,
        null=True,
    )

    banner = models.ImageField(
        upload_to='user-banners/',
        blank=True,
        null=True,
    )

