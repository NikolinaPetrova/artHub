from django.db import models


class JoinPolicy(models.TextChoices):
    OPEN = 'open', 'Open'
    APPROVAL = 'approval', 'Approval required'


class RoleChoices(models.TextChoices):
    MEMBER = 'member', 'Member'
    MODERATOR = 'moderator', 'Moderator'
    ADMIN = 'admin', 'Admin'


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'