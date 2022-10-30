from rest_framework import serializers

import pdf_crawler.apps.crawler.models as crawler_models


__all__ = [
    'DocumentListSerializer',
    'LinkListSerializer',
    'UrlSerializer',
    'DocumentUrlsSerializer',
    'FileSerializer'
]


class DocumentListSerializer(serializers.ModelSerializer):
    """
    Serializer for documents list
    """
    number_of_urls = serializers.IntegerField()

    class Meta:
        model = crawler_models.Document
        fields = ('id', 'name', 'number_of_urls')


class LinkListSerializer(serializers.ModelSerializer):
    """
    Serializer for urls list
    """
    number_of_documents = serializers.IntegerField()

    class Meta:
        model = crawler_models.Link
        fields = ('url', 'number_of_documents', 'is_alive')


class UrlSerializer(serializers.ModelSerializer):
    """
    Serializer for single link object
    """

    class Meta:
        model = crawler_models.Link
        fields = ('url', 'is_alive')


class DocumentUrlsSerializer(serializers.ModelSerializer):
    """
    Serializer for single document urls
    """
    urls = UrlSerializer(source='links', many=True)

    class Meta:
        model = crawler_models.Document
        fields = ('urls', )


class FileSerializer(serializers.Serializer):

    file = serializers.FileField(use_url=False)
