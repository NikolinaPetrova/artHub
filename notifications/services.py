from django.urls import reverse
from artworks.models import Artwork
from groups.choices import RoleChoices
from groups.models import Post
from interactions.models import Comment
from notifications.choices import NotificationsChoices
from notifications.models import Notification


class NotificationService:
    @staticmethod
    def get_artwork_url(artwork):
        return reverse('artwork-details', kwargs={'pk': artwork.pk})

    @staticmethod
    def get_post_url(post):
        return reverse('post-details', kwargs={'slug': post.group.slug, 'pk': post.pk})

    @staticmethod
    def get_group_url(group, tab=None):
        url = reverse('group-details', kwargs={'slug': group.slug})
        if tab:
            url += f'?tab={tab}'
        return url

    @classmethod
    def get_comment_target_url(cls, comment):
        if comment.artwork:
            return cls.get_artwork_url(comment.artwork)

        if comment.post:
            return cls.get_post_url(comment.post)

        return '#'

    @staticmethod
    def create(
            *,
            recipient,
            sender,
            notification_type,
            message,
            artwork=None,
            post=None,
            comment=None,
            target_url='#'
    ):
        return Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            message=message,
            artwork=artwork,
            post=post,
            comment=comment,
            target_url=target_url
        )

    @classmethod
    def create_if_not_sender(cls, *, recipient, sender, **kwargs):
        if recipient == sender:
            return None
        return cls.create(recipient=recipient, sender=sender, **kwargs)

    @staticmethod
    def bulk_create(notifications):
        if notifications:
            Notification.objects.bulk_create(notifications)

    @classmethod
    def notify_comment(cls, comment):
        sender = comment.user
        target_url = cls.get_comment_target_url(comment)
        notified_user_ids = set()

        if comment.artwork:
            recipient = comment.artwork.user
            created = cls.create_if_not_sender(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.COMMENT_ARTWORK,
                message=f"{sender.username} commented on your artwork",
                artwork=comment.artwork,
                comment=comment,
                target_url=target_url
            )
            if created:
                notified_user_ids.add(recipient.pk)

        elif comment.post:
            recipient = comment.post.author
            created = cls.create_if_not_sender(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.COMMENT_POST,
                message=f"{sender.username} commented on your post",
                post=comment.post,
                comment=comment,
                target_url=target_url
            )
            if created:
                notified_user_ids.add(recipient.pk)

        current = comment.parent
        while current:
            user = current.user
            if user != sender and user.pk not in notified_user_ids:
                cls.create(
                    recipient=user,
                    sender=sender,
                    notification_type=NotificationsChoices.REPLY,
                    message=(
                        f"{sender.username} replied to your comment"
                        if current == comment.parent
                        else f"{sender.username} replied in a thread you're in"
                    ),
                    comment=comment,
                    post=comment.post if comment.post else None,
                    artwork=comment.artwork if comment.artwork else None,
                    target_url=target_url
                )
                notified_user_ids.add(user.pk)
            current = current.parent


    @classmethod
    def notify_like(cls, obj, sender):
        notification_type = None
        owner = None
        target_url = '#'
        artwork = None
        post = None
        comment = None
        object_name = obj.__class__.__name__.lower()

        if isinstance(obj, Artwork):
            owner = obj.user
            notification_type = NotificationsChoices.LIKE_ARTWORK
            target_url = cls.get_artwork_url(obj)
            artwork = obj

        elif isinstance(obj, Post):
            owner = obj.author
            notification_type = NotificationsChoices.LIKE_POST
            target_url = cls.get_post_url(obj)
            post = obj

        elif isinstance(obj, Comment):
            owner = obj.user
            notification_type = NotificationsChoices.LIKE_COMMENT
            target_url = cls.get_comment_target_url(obj)
            comment = obj
            artwork = obj.artwork if obj.artwork else None
            post = obj.post if obj.post else None

        if not owner or owner == sender or not notification_type:
            return

        cls.create(
            recipient=owner,
            sender=sender,
            notification_type=notification_type,
            message=f"{sender.username} liked your {object_name}",
            artwork=artwork,
            post=post,
            comment=comment,
            target_url=target_url
        )

    @classmethod
    def notify_new_post(cls, post):
        group = post.group
        sender = post.author
        target_url = cls.get_post_url(post)
        members = group.members.exclude(user=sender).select_related('user')

        notifications = [
            Notification(
                recipient=member.user,
                sender=sender,
                notification_type=NotificationsChoices.NEW_POST,
                message=f'{sender.username} created a new post in {group.name}',
                post=post,
                target_url=target_url
            )
            for member in members
        ]
        cls.bulk_create(notifications)

    @classmethod
    def notify_join_to_public_group(cls, sender, group):
        cls.create_if_not_sender(
            recipient=group.owner,
            sender=sender,
            notification_type=NotificationsChoices.JOIN_PUBLIC_GROUP,
            message=f"{sender.username} joined your public group {group.name}",
            target_url=cls.get_group_url(group, tab='members'),
        )

    @classmethod
    def notify_join_request(cls, sender, group):
        cls.create_if_not_sender(
            recipient=group.owner,
            sender=sender,
            notification_type=NotificationsChoices.JOIN_REQUEST,
            message=f'{sender.username} wants to join your private group {group.name}',
            target_url=cls.get_group_url(group, tab='joinRequests'),
        )

    @classmethod
    def notify_join_approved(cls, sender, group, recipient):
        cls.create_if_not_sender(
            recipient=recipient,
            sender=sender,
            notification_type=NotificationsChoices.JOIN_APPROVED,
            message=f"{sender.username} approved your request to join {group.name}",
            target_url=cls.get_group_url(group),
        )

    @classmethod
    def notify_join_rejected(cls, sender, group, recipient):
        cls.create_if_not_sender(
            recipient=recipient,
            sender=sender,
            notification_type=NotificationsChoices.JOIN_REJECTED,
            message=f'{sender.username} rejected your request to join {group.name}',
            target_url=cls.get_group_url(group),
        )

    @classmethod
    def notify_submission(cls, sender, group, artwork):
        admins = group.members.filter(
            role__in=[RoleChoices.ADMIN, RoleChoices.MODERATOR]
        ).exclude(user=sender).select_related('user')


        target_url = cls.get_group_url(group, tab='submissions')

        notifications = [
            Notification(
                recipient=member.user,
                sender=sender,
                notification_type=NotificationsChoices.SUBMISSION,
                message=f'{sender.username} submitted artwork to {group.name}',
                artwork=artwork,
                target_url=target_url
            )
            for member in admins
        ]
        cls.bulk_create(notifications)

    @classmethod
    def notify_submission_approved(cls, reviewed_by, group, recipient, artwork):
        cls.create_if_not_sender(
            recipient=recipient,
            sender=reviewed_by,
            notification_type=NotificationsChoices.SUBMISSION_APPROVED,
            message=f'Your artwork {artwork} has been approved in {group.name}',
            target_url=cls.get_group_url(group)
        )

    @classmethod
    def notify_submission_rejected(cls, reviewed_by, group, recipient, artwork):
        cls.create_if_not_sender(
            recipient=recipient,
            sender=reviewed_by,
            notification_type=NotificationsChoices.SUBMISSION_REJECTED,
            message=f"Your artwork {artwork} has been rejected from {group.name}",
            target_url=cls.get_artwork_url(artwork)
        )