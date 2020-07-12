"""helitrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

import accounts.views as account_views
import decks.views as deck_views
import inspections.views as inspections_views

schema_view = get_swagger_view(title='Helitrack API')

router = DefaultRouter()
router.register(r'users', account_views.UserViewSet, basename='user')
router.register(r'groups', account_views.GroupViewSet, basename='group')
router.register(r'inspections', inspections_views.InspectionViewSet, basename='inspection')
router.register(r'inspection-statuses', inspections_views.StatusViewSet, basename='status')
router.register(r'inspection-types', inspections_views.InspectionTypeViewSet, basename='inspection_type')

router.register(r'decks', deck_views.DeckViewSet, basename='deck')
router.register(r'clusters', deck_views.ClusterViewSet, basename='cluster')
router.register(r'operators', deck_views.OperatorViewSet, basename='operator')

router.register(r'reports', inspections_views.ReportViewSet, basename='report')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/data/', include('data.urls')),
    path('api/v1/', include(router.urls)),
    url('api/swagger/', schema_view),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
