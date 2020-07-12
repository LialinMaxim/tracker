from rest_framework import serializers

from .models import Cluster, Operator, Deck


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        exclude = ('updated', 'author')


class ClusterReportPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('id', 'title',)


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        exclude = ('updated',)


class DeckSerializer(serializers.ModelSerializer):
    cluster = ClusterSerializer
    operator = OperatorSerializer

    class Meta:
        model = Deck
        exclude = ('updated',)


class DeckReportPreviewSerializer(serializers.ModelSerializer):
    cluster = ClusterReportPreviewSerializer(read_only=True)

    class Meta:
        model = Deck
        fields = ('id', 'title', 'is_manned', 'is_offshore', 'cluster')
