from rest_framework import serializers
from .models import CheckResults, SchemaDefinitions, Notification


class CheckResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckResults
        fields = ("user_id", "data", "created_at")


class SchemaDefinitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaDefinitions
        fields = ("name", "data")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("text", "created_at", "is_read")
