from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    reference_id = serializers.CharField()
    status = serializers.CharField()
