from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source='sender.username',
        read_only=True
    )

    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'sender_username',
            'notification_type',
            'message',
            'target_url',
            'is_read',
            'created_at',
            'sender_avatar',
        ]

        read_only_fields = ['id', 'message', 'target_url', 'created_at']

    def get_sender_avatar(self, obj):
        if obj.sender.profile.avatar:
            return obj.sender.profile.avatar.url
        return None