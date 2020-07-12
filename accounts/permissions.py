from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import GroupLevel


class IsPaidUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.payment_info:
            return True


def HasRoleDecorator(role):
    class HasRole(BasePermission):
        def has_permission(self, request, view):
            if request.user and request.user.role == role:
                return True

    return HasRole


class AllowedByGroupLevel(BasePermission):
    message = 'Your permission group is not allowed.'

    def has_permission(self, request, view):
        if request.user.is_superuser or (request.method in SAFE_METHODS):
            return True

        user_level = self.get_user_max_level(request)
        data_level = self.get_data_request_max_level(request)

        return bool(
            user_level > data_level and
            self.is_valid_clusters(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (request.method in SAFE_METHODS):
            return True

        # only superuser can edit superuser
        if obj.is_superuser:
            return False

        obj_level = max([0] + [self.get_level(group) for group in obj.groups.all()])
        user_level = self.get_user_max_level(request)
        data_level = self.get_data_request_max_level(request)

        return bool(
            user_level > obj_level and
            user_level > data_level and
            self.is_valid_clusters(request)
        )

    @staticmethod
    def get_level(group):
        if getattr(group, 'grouplevel', None):
            return group.grouplevel.level
        return 0

    def is_valid_clusters(self, request):
        # admin group can set any clusters to other users
        if self.get_user_max_level(request) == self.get_max_groups_level():
            return True

        # other group can set theirs cluster to other users
        user_clusters_ids = [cluster.id for cluster in request.user.clusters.all()]
        request_clusters_ids = request.data.get('clusters', [])
        for cluster_id in request_clusters_ids:
            if cluster_id not in user_clusters_ids:
                return False
        return True

    @staticmethod
    def get_max_groups_level():
        return GroupLevel.objects.order_by('level').last().level

    @staticmethod
    def get_data_request_max_level(request):
        groups = request.data.get('groups', [])
        if isinstance(groups, int) or isinstance(groups, str):
            groups = [int(groups)]
        levels = GroupLevel.objects.filter(group_id__in=groups).all()
        return max([0] + [lg.level for lg in levels])

    def get_user_max_level(self, request):
        return max([0] + [self.get_level(group) for group in request.user.groups.all()])
