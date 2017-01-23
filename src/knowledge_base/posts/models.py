# -*- coding: utf-8 -*-
import os
from hashlib import md5

from django.conf import settings
from django.db import models

from knowledge_base.core.db.models import CatalogueMixin


def get_area_image_path(instance, filename):
    """
    Get the upload path to the profile image.
    """
    return '{0}/{1}{2}'.format(
        "areas/originals",
        md5(filename).hexdigest(),
        os.path.splitext(filename)[-1]
    )


def get_area_thumbnail_path(instance, filename):
    """
    Get the proper upload path to the thumbnail profile image.
    """
    return '{0}/{1}'.format(
        "areas/thumbnails",
        filename
    )


class Area(CatalogueMixin):
    """
    Areas of the knowledge base.
    """
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )

    photo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_area_image_path
    )

    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_area_thumbnail_path
    )


class Subject(CatalogueMixin):
    """
    Subjects that belongs to each area.
    """
    area = models.ForeignKey(
        Area,
        related_name='subjects'
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )


class Post(CatalogueMixin):
    """
    Main model of the application, is essentially information of a subject.
    """
    subject = models.ForeignKey(
        Subject,
        related_name='posts'
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        verbose_name='author'
    )
