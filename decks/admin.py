from django.contrib import admin

from .models import Cluster, Operator, Deck


@admin.register(Operator)
class InspectionOptionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated']
    list_filter = ['updated']
    search_fields = ['title']


@admin.register(Cluster)
class InspectionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'is_permanent',
        'updated',
    ]
    list_filter = ['is_permanent', 'updated']
    search_fields = ['title', 'description']


@admin.register(Deck)
class InspectionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'operator',
        'cluster',
        't_value',
        'position_latitude',
        'position_longitude',
        'is_manned',
        'is_offshore',
        'updated',
    ]
    list_filter = ['is_manned', 'is_offshore', 'updated']
    search_fields = ['title']
