from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from data.models import Notification
from inspections.permissions import NotChangedInspectionType
from .filter import ReportFilter
from .validators import validate_groups
from .models import Inspection, Status, Report, InspectionType
from .serializers import (InspectionSerializer, InspectionStatusSerializer, ReportSerializer,
                          InspectionTypeSerializer, ReportPreviewSerializer)


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = InspectionStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class InspectionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InspectionType.objects.all()
    serializer_class = InspectionTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def list(self, request, *args, **kwargs):
        queryset = InspectionType.objects.values('id', 'title').all()
        serializer = InspectionTypeSerializer(queryset, many=True)
        return Response(serializer.data)


class InspectionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions, NotChangedInspectionType)
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.permission_groups_filtered_queryset(request)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def types_statuses(self, request):
        statuses = InspectionStatusSerializer(Status.objects.all(), many=True)
        types = InspectionTypeSerializer(InspectionType.objects.values('id', 'title').all(), many=True)

        return Response({
            "statuses": statuses.data,
            "types": types.data,
        })

    @action(url_path='(?P<id_inspection>\d+)/report', methods=['get'], detail=False)
    def report(self, request, id_inspection=None):
        queryset = Report.objects.filter(inspection=id_inspection).all()
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def permission_groups_filtered_queryset(request):
        # Administer group
        if request.user.is_superuser or request.user.is_administer():
            return Inspection.objects.all()

        # Inspector group can see assigned to him inspection only.
        if request.user.is_inspector():
            return Inspection.objects.filter(user_assigned=request.user).all()

        # Director and Manager group
        return Inspection.objects.filter(
            deck__cluster__in=request.user.clusters.all()
        ).all()


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ReportFilter
    search_fields = ('inspection__deck__title', 'inspection__deck__designator')

    def create(self, request, *args, **kwargs):
        """
        One inspection have one report only.
        """
        inspection = get_object_or_404(Inspection, pk=int(request.data.get('inspection')))
        groups, groups_preview, colors_set, values_set = validate_groups(request.data.get('groups'))
        report = Report.objects.filter(inspection=inspection.id).last()
        if not report:
            # create new report
            report = Report.objects.create(
                inspection=inspection,
                groups=groups,
                groups_preview=groups_preview,
                colors_set=colors_set,
                values_set=values_set,
            )
        else:
            # update exist report
            report.groups = groups
            report.groups_preview = groups_preview
            report.colors_set = colors_set
            report.values_set = values_set
            report.save()

        Notification.objects.create(
            user=inspection.author,
            text=f'{str(inspection.user_assigned.username).title()} submitted new {inspection.type} report'
        )
        serializer = self.serializer_class(report)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk)

        if request.data.get('inspection'):
            inspection = get_object_or_404(Inspection, pk=int(request.data.get('inspection')))
            report.inspection = inspection

        if request.data.get('groups'):
            groups, groups_preview, colors_set, values_set = validate_groups(request.data.get('groups'))
            report.groups = groups
            report.groups_preview = groups_preview
            report.colors_set = colors_set
            report.values_set = values_set

        report.save()
        serializer = self.serializer_class(report)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk)
        inspection = get_object_or_404(Inspection, pk=int(request.data.get('inspection')))
        groups, groups_preview, colors_set, values_set = validate_groups(request.data.get('groups'))

        report.inspection = inspection
        report.groups = groups
        report.groups_preview = groups_preview
        report.colors_set = colors_set
        report.values_set = values_set
        report.save()

        serializer = self.serializer_class(report)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.permission_groups_filtered_queryset(request)
        )
        serializer = ReportPreviewSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def permission_groups_filtered_queryset(request):
        # Administer group
        if request.user.is_superuser or request.user.is_administer():
            return Report.objects.all()

        # Inspector group
        if request.user.is_inspector():
            return Report.objects.filter(inspection__user_assigned=request.user).all()

        # Director and Manager group
        return Report.objects.filter(
            inspection__deck__cluster__in=request.user.clusters.all()
        ).all()
