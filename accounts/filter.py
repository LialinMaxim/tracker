from django_filters import rest_framework as filters
import json
from django.contrib.auth.models import Group
from accounts.models import User


class UserFilter(filters.FilterSet):
    group = filters.CharFilter(method='filter_by_groups')
    username = filters.CharFilter('username', 'istartswith')
    email = filters.CharFilter('email', 'istartswith')
    alias = filters.CharFilter('alias', 'istartswith')

    def filter_by_groups(self, queryset, name, value):
        try:
            ids = json.loads(value)
        except Exception:
            raise Exception("JSON in groups filter is invalid")

        return queryset.filter(groups__pk__in=ids)

    class Meta:
        model = User
        fields = ('username', 'group', 'alias')
