
import re
from django.db.models.aggregates import Count
from django.db import transaction
from rest_framework import views
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import pdf_crawler.apps.crawler.models as crawler_models
import pdf_crawler.apps.crawler.serializers as crawler_serializers
import pdf_crawler.apps.crawler.utils as crawler_utils

__all__ = [
    'FileUploadView',
    'DocumentListAPIView',
    'LinkListAPIView',
    'DocumentUrlsApiView',
]


class FileUploadView(views.APIView):
    """
    View for upload pdf document, parse it and store unique data
    """
    serializer = crawler_serializers.FileSerializer

    def post(self, request, version):

        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        pdf_file = data['file']

        # Get pdf data
        pdf_file_text = crawler_utils.pdf_to_text(pdf_file)

        # Get all urls from pdf file
        urls = re.findall(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            pdf_file_text
        )
        urls_with_status = []
        for url in urls:
            urls_with_status.append({'url': url, 'is_alive': crawler_utils.check_url(url)})

        # If this file was uploaded previously - don`t repeat it
        if crawler_models.Document.objects.filter(file_size=len(pdf_file), name=pdf_file.name).exists():
            return Response(status=200, data={'This file has already been uploaded'})

        # For new file - we create document
        with transaction.atomic():
            pdf_doc = crawler_models.Document.objects.create(name=pdf_file.name, file_size=len(pdf_file))
            for url_with_status in urls_with_status:
                link = crawler_models.Link.objects.filter(url=url_with_status['url']).last()

                # If its new url - save it in DB
                if not link:
                    link = crawler_models.Link.objects.create(
                        url=url_with_status['url'],
                        is_alive=url_with_status['is_alive']
                    )

                # If url exist in pdf file - add it to document
                if link:
                    pdf_doc.links.add(link)

        return Response(status=200, data={'This file was uploaded successfully'})


class DocumentListAPIView(ListAPIView):
    """
    Return list of documents with some document data
    """
    queryset = crawler_models.Document.objects.annotate(number_of_urls=Count('links')).all()
    serializer_class = crawler_serializers.DocumentListSerializer
    permission_classes = (AllowAny,)


class LinkListAPIView(ListAPIView):
    """
    Return list of links
    """
    queryset = crawler_models.Link.objects.annotate(number_of_documents=Count('documents')).all()
    serializer_class = crawler_serializers.LinkListSerializer
    permission_classes = (AllowAny,)


class DocumentUrlsApiView(RetrieveAPIView):
    """
    Return some data for current  document
    """
    permission_classes = (AllowAny, )
    queryset = crawler_models.Document.objects.all()
    serializer_class = crawler_serializers.DocumentUrlsSerializer
    lookup_field = 'pk'
