from django.contrib import admin

from .models import Status, Inspection, Report, InspectionType


@admin.register(Status, InspectionType)
class InspectionOptionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated']
    list_filter = ['updated']
    search_fields = ['title']


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'user_assigned',
        'scheduled_by',
        'status',
        'type',
        'deck',
        'due_date',
        'completed_date',
        'updated',
        'is_archived',
    ]
    list_filter = ['is_archived', 'updated']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'inspection',
        'groups_preview',
        'updated',
    ]
    list_filter = ['updated']
