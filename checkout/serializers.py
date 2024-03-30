from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    data = serializers.JSONField()
