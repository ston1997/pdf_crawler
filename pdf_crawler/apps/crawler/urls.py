from django.conf.urls import url

import pdf_crawler.apps.crawler.views as crawler_views

urlpatterns = [
    url(r'^document/upload/$', crawler_views.FileUploadView.as_view(), name='document-upload'),
    url(r'^document/list/$', crawler_views.DocumentListAPIView.as_view(), name='documents-list'),
    url(r'^link/list/$', crawler_views.LinkListAPIView.as_view(), name='links-list'),
    url(
        r'^document/urls/(?P<pk>[0-9a-f-]+)/$', crawler_views.DocumentUrlsApiView.as_view(), name='document-urls'
    ),
]
