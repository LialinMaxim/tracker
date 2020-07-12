from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CheckResults, SchemaDefinitions, Notification
from .pagination import StandardResultsSetPagination
from .serializers import CheckResultsSerializer, SchemaDefinitionsSerializer, NotificationSerializer


class CheckResultsView(generics.ListCreateAPIView):
    # /data/checkresults
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = CheckResultsSerializer

    def get_queryset(self):
        return CheckResults.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        Notification.objects.create(
            user=self.request.user, text='New check result'
        )

        return serializer.save(user=self.request.user)  # field `data` is stored automatically


class SchemaDefinitionsView(generics.RetrieveAPIView):
    # /data/schemas
    permission_classes = tuple()
    serializer_class = SchemaDefinitionsSerializer

    queryset = SchemaDefinitions.objects.all()
    lookup_field = 'name'


class NotificationsView(generics.ListAPIView):
    # /data/notifications
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationsRead(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, ):
        Notification.objects.filter(user=self.request.user).update(is_read=True)
        return Response({}, status=status.HTTP_200_OK)
