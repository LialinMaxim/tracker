import json
import operator
from functools import reduce

from django_filters import rest_framework as filters
from django.db.models import Q


class ReportFilter(filters.FilterSet):
    type_id = filters.CharFilter('inspection__type__id', 'exact')
    type_title = filters.CharFilter('inspection__type__title', 'exact')
    inspection_id = filters.CharFilter('inspection__id', 'exact')
    deck_id = filters.CharFilter('inspection__deck__id', 'exact')
    contains_colors = filters.CharFilter(method='filter_by_colors')
    contains_values = filters.CharFilter(method='filter_by_values')

    @staticmethod
    def validate_json(value, field_name):
        try:
            data_list = json.loads(str(value).lower())
        except Exception:
            raise Exception(f"JSON filter {field_name} is invalid.")
        return data_list

    def filter_by_colors(self, queryset, field_name, value):
        data_list = self.validate_json(value, field_name)
        return queryset.filter(
            reduce(
                operator.and_,
                (Q(colors_set__contains=value) for value in data_list)
            ))

    def filter_by_values(self, queryset, field_name, value):
        data_list = self.validate_json(value, field_name)
        return queryset.filter(
            reduce(
                operator.and_,
                (Q(values_set__contains=value) for value in data_list)
            ))
