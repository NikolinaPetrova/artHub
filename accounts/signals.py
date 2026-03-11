from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from albums.models import Album

UserModel = settings.AUTH_USER_MODEL

@receiver(post_save, sender=UserModel)
def create_default_album(sender, instance, created, **kwargs):
    if created and not Album.objects.filter(owner=instance, name='Default Album').exists():
        Album.objects.create(
            owner=instance,
            name='Default Album'
        )


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)