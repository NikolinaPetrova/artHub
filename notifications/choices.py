from django.db import models


class NotificationsChoices(models.TextChoices):
	JOIN_REQUEST = 'join_request', 'Join Request'
	JOIN_APPROVED = 'join_approved', 'Join Approved'
	JOIN_REJECTED = 'join_rejected', 'Join Rejected'
	NEW_MEMBER = 'new_member', 'New Member Joined'
	SUBMISSION = 'submission', 'Artwork Submission'
	SUBMISSION_APPROVED = 'submission_approved', 'Submission Approved'
	SUBMISSION_REJECTED = 'submission_rejected', 'Submission Rejected'
	LIKE_ARTWORK = 'like_artwork', 'Like Artwork'
	LIKE_COMMENT = 'like_comment', 'Like Comment'
	LIKE_POST = 'like_post', 'Like Post'
	COMMENT_ARTWORK = 'comment_artwork', 'Comment Artwork'
	COMMENT_POST = 'comment_post', 'Comment Post'
	REPLY = 'reply', 'Reply to Comment'
	NEW_POST = 'new_post', 'New Post in Group'