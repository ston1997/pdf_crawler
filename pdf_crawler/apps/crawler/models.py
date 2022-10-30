from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    'Link',
    'Document'
]


class Link(models.Model):
    """
    Model for store documents links
    """

    url = models.URLField(
        max_length=256,
        null=False,
        verbose_name=_('url'),

    )
    is_alive = models.BooleanField(
        default=False,
        verbose_name=_('is_alive')
    )


class Document(models.Model):
    """
    Model for store some document attribute data
    """

    dt_created = models.DateTimeField(
        auto_now=True,
        verbose_name=_('dt_created'),
    )
    name = models.CharField(
        max_length=256,
        null=False,
        verbose_name=_('name')
    )
    links = models.ManyToManyField(
        Link,
        related_name='documents',
        verbose_name=_('links')
    )
    file_size = models.BigIntegerField(
        null=False,
        verbose_name=_('file_size')
    )
