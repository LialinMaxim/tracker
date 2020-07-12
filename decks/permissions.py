from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInspector(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.vessel
        )

    def has_object_permission(self, request, view, obj):
        # Instance must have .author attribute
        return bool(
            request.method in SAFE_METHODS or
            obj.author == request.user
        )
