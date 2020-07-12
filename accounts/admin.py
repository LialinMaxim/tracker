from django.contrib import admin

from .models import User, GroupLevel


@admin.register(User)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'vessel',
        'is_superuser',
        'date_joined',
        'last_login',
    )
    list_filter = ('vessel',)
    search_fields = ('email', 'username')


@admin.register(GroupLevel)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('group', 'level')
    list_editable = ('level',)
