from django.db.models import Q
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response

from inspections.models import Inspection
from .models import Cluster, Operator, Deck
from .serializers import ClusterSerializer, OperatorSerializer, DeckSerializer
from .permissions import IsInspector


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = (permissions.DjangoModelPermissions, IsInspector,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def perform_create(self, serializer):
        """
        Creates a new cluster object and adds it to the current user.
        """
        new_cluster = serializer.save(author=self.request.user)
        self.request.user.clusters.add(new_cluster)


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def list(self, request, *args, **kwargs):
        queryset = self.permission_groups_filtered_queryset(request)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def permission_groups_filtered_queryset(request):
        # Administer group
        if request.user.is_superuser or request.user.is_administer():
            return Deck.objects.all()

        # Inspector group
        if request.user.is_inspector():
            assigned_inspections = Inspection.objects.filter(user_assigned=request.user).all()
            if request.user.vessel:
                # inspector can see all decs with allowed clusters or from assigned to him inspections
                pks = [i.deck.id for i in assigned_inspections]
                return Deck.objects.filter(
                    Q(id__in=pks) | Q(cluster__in=request.user.clusters.all())
                ).all()
            else:
                # inspector can see all decks from assigned to him inspections
                return [i.deck for i in assigned_inspections]

        # Director and Manager group
        return Deck.objects.filter(
            cluster__in=request.user.clusters.all()
        ).all()
