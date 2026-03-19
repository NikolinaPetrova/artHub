from django.urls import reverse
from artworks.models import Artwork
from groups.choices import RoleChoices
from groups.models import Post
from interactions.models import Comment
from notifications.choices import NotificationsChoices
from notifications.models import Notification


class NotificationService:
    @staticmethod
    def create(
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
    def notify_comment(cls, comment):
        sender = comment.user

        if comment.artwork:
            recipient = comment.artwork.user
        else:
            recipient = comment.post.author

        notified_users = set()

        def _get_target_url(comment):
            if comment.artwork:
                return reverse('artwork-details', kwargs={'pk': comment.artwork.pk})
            return reverse('post-details', kwargs={
                'slug': comment.post.group.slug,
                'pk': comment.post.pk
            })

        if comment.artwork and recipient != sender:
            cls.create(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.COMMENT_ARTWORK,
                message=f"{sender.username} commented on your artwork",
                artwork=comment.artwork,
                comment=comment,
                target_url=_get_target_url(comment)
            )
            notified_users.add(recipient.pk)

        if comment.post and recipient != sender:
            cls.create(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.COMMENT_POST,
                message=f"{sender.username} commented on your post",
                post=comment.post,
                comment=comment,
                target_url=_get_target_url(comment)
            )

            notified_users.add(recipient.pk)

        current = comment.parent
        while current:
            user = current.user
            if user != sender and user.pk not in notified_users:
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
                    target_url=_get_target_url(comment)
                )
                notified_users.add(user.pk)
            current = current.parent


    @classmethod
    def notify_like(cls, obj, sender):
        if isinstance(obj, Post):
            owner = obj.author
        else:
            owner = obj.user

        if owner == sender:
            return

        notification_type = None
        target_url = '#'

        if isinstance(obj, Artwork):
            notification_type = NotificationsChoices.LIKE_ARTWORK
            target_url = reverse('artwork-details', kwargs={'pk': obj.pk})

        elif isinstance(obj, Post):
            notification_type = NotificationsChoices.LIKE_POST
            target_url = reverse('post-details', kwargs={'slug': obj.group.slug, 'pk': obj.pk})

        elif isinstance(obj, Comment):
            notification_type = NotificationsChoices.LIKE_COMMENT
            target_url = (
                reverse('artwork-details', kwargs={'pk': obj.artwork.pk})
                if obj.artwork
                else reverse('post-details', kwargs={'slug': obj.group.slug, 'pk': obj.pk})
            )

        cls.create(
            recipient=owner,
            sender=sender,
            notification_type=notification_type,
            message=f"{sender.username} liked your {obj.__class__.__name__.lower()}",
            artwork=obj if isinstance(obj, Artwork) else None,
            post=obj if isinstance(obj, Post) else None,
            comment=obj if isinstance(obj, Comment) else None,
            target_url=target_url
        )

    @classmethod
    def notify_new_post(cls, post):
        group = post.group
        sender = post.author

        members = group.members.exclude(user=sender)

        for member in members:
            cls.create(
                recipient=member.user,
                sender=sender,
                notification_type=NotificationsChoices.NEW_POST,
                message=f"{sender.username} created a new post in {group.name}",
                post=post,
                target_url=reverse('post-details', kwargs={'slug': post.group.slug, 'pk': post.pk})
            )

    @classmethod
    def notify_join_to_public_group(cls, sender, group):
        if sender != group.owner:
            cls.create(
                recipient=group.owner,
                sender=sender,
                notification_type=NotificationsChoices.JOIN_PUBLIC_GROUP,
                message=f"{sender.username} joined to your public group {group.name}",
                target_url=reverse('group-details', kwargs={'slug': group.slug}) + '?tab=members'
            )

    @classmethod
    def notify_join_request(cls, sender, group):
        if sender != group.owner:
            cls.create(
                recipient=group.owner,
                sender=sender,
                notification_type=NotificationsChoices.JOIN_REQUEST,
                message=f"{sender.username} wants to join your private group {group.name}",
                target_url=reverse('group-details', kwargs={'slug': group.slug}) + '?tab=joinRequests'
            )

    @classmethod
    def notify_join_approved(cls, sender, group, recipient):
        if sender != recipient:
            cls.create(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.JOIN_APPROVED,
                message=f"{group.owner} approved you to join {group.name}",
                target_url=reverse('group-details', kwargs={'slug': group.slug})
            )

    @classmethod
    def notify_join_rejected(cls, sender, group, recipient):
        if sender != recipient:
            cls.create(
                recipient=recipient,
                sender=sender,
                notification_type=NotificationsChoices.JOIN_REJECTED,
                message=f"{group.owner} rejected you to join {group.name}",
                target_url=reverse('group-details', kwargs={'slug': group.slug})
            )

    @classmethod
    def notify_submission(cls, sender, group, artwork):
        admins = group.members.filter(role__in=[RoleChoices.ADMIN, RoleChoices.MODERATOR])

        for member in admins:
            cls.create(
                recipient=member.user,
                sender=sender,
                notification_type=NotificationsChoices.SUBMISSION,
                message=f"{sender.username} submitted artwork to {group.name}",
                artwork=artwork,
                target_url=reverse('group-details', kwargs={'slug': group.slug}) + '?tab=submissions'
            )

    @classmethod
    def notify_submission_approved(cls, reviewed_by, group, recipient, artwork):
        if reviewed_by != recipient:
            cls.create(
                recipient=recipient,
                sender=reviewed_by,
                notification_type=NotificationsChoices.SUBMISSION_APPROVED,
                message=f"Your artwork {artwork} has been approved to group {group.name}",
                target_url = reverse('group-details', kwargs={'slug': group.slug})
            )

    @classmethod
    def notify_submission_rejected(cls, reviewed_by, group, recipient, artwork):
        if reviewed_by != recipient:
            cls.create(
                recipient=recipient,
                sender=reviewed_by,
                notification_type=NotificationsChoices.SUBMISSION_REJECTED,
                message=f"Your artwork {artwork} has been rejected from group {group.name}",
                target_url = reverse('artwork-details', kwargs={'pk': artwork.pk})
            )