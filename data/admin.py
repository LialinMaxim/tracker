from django.contrib import admin

from .models import CheckResults, SchemaDefinitions, Notification

admin.site.register(CheckResults)
admin.site.register(SchemaDefinitions)
admin.site.register(Notification)
