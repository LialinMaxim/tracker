from rest_framework import serializers

from decks.serializers import DeckSerializer, DeckReportPreviewSerializer
from .models import Inspection, Status, Report, InspectionType


class InspectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        exclude = ('updated',)


class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        exclude = ('updated',)


class InspectionTypeNoSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        exclude = ('updated', 'schema')


class InspectionSerializer(serializers.ModelSerializer):
    deck = DeckSerializer
    status = InspectionStatusSerializer
    type = InspectionTypeNoSchemaSerializer

    class Meta:
        model = Inspection
        exclude = ('updated',)


class InspectionReportSerializer(serializers.ModelSerializer):
    deck = DeckReportPreviewSerializer(read_only=True)
    type = InspectionTypeNoSchemaSerializer(read_only=True)

    class Meta:
        model = Inspection
        fields = ('id', 'deck', 'is_archived', 'type',)


class ReportSerializer(serializers.ModelSerializer):
    inspection = InspectionSerializer

    class Meta:
        model = Report
        fields = ('id', 'groups', 'inspection', 'updated')


class ReportPreviewSerializer(serializers.ModelSerializer):
    inspection = InspectionReportSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'groups_preview', 'inspection', 'updated')
