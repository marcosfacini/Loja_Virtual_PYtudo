from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    notificationCode = serializers.CharField()
    notificationType = serializers.CharField()
