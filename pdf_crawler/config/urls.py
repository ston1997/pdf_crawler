"""pdf_crawler URL Configuration
"""
from django.conf.urls import url, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


api_urlpatterns = [

    url(r'', include('pdf_crawler.apps.crawler.urls', namespace='crawler')),
]


urlpatterns = [

    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^readoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    url(r'^api/(?P<version>(v1|v2))/', include(api_urlpatterns, namespace='api')),
]
