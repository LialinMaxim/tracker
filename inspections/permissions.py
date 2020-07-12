from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import GroupLevel


class NotChangedInspectionType(BasePermission):
    message = 'You can not change inspection type'

    def has_object_permission(self, request, view, obj):
        if not str(request.data.get('type')) == str(getattr(obj, 'type_id')):
            return False
        return True
