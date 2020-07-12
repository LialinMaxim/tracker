from django.urls import path
from .views import CheckResultsView, SchemaDefinitionsView, NotificationsView, NotificationsRead


urlpatterns = [
    path('checkresults/', CheckResultsView.as_view(), name="data-checkresults"),
    path(r'schemas/<str:name>', SchemaDefinitionsView.as_view(), name="data-schemas"),
    path('notifications/', NotificationsView.as_view(), name="data-notifications"),
    path('notifications/read', NotificationsRead.as_view(), name="data-notifications-read")
]
