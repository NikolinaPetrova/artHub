from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, post_migrate
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


@receiver(post_migrate)
def assign_permissions_to_content_groups(sender, **kwargs):
    if sender.name != 'accounts':
        return

    moderators_group, _ = Group.objects.get_or_create(name='Content Moderator')
    editors_group, _ = Group.objects.get_or_create(name='Content Editor')

    editors_permissions = [
        ('artworks', 'change_artwork'),
        ('albums', 'change_album'),
        ('interactions', 'change_comment'),
        ('groups', 'change_post'),
        ('groups', 'change_group')
    ]

    moderators_permissions = [
        ('accounts', 'delete_arthubuser'),
        ('accounts', 'delete_profile'),
        ('artworks', 'delete_artwork'),
        ('albums', 'delete_album'),
        ('interactions', 'delete_comment'),
        ('groups', 'delete_post'),
        ('groups', 'delete_group'),
    ]

    for app_label, codename in editors_permissions:
        try:
            perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            editors_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass

    for app_label, codename in moderators_permissions:
        try:
            perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            moderators_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass
