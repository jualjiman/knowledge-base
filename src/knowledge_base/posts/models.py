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

    @property
    def thumbnail_settings(self):
        """
        Property used to configurate thumbnail creation settings.
        """
        return {
            "dimension": "300x200",
            "original_field": "photo",
            "thumbnail_field": "thumbnail"
        }


class Category(CatalogueMixin):
    """
    Category that belongs to each area.
    """
    area = models.ForeignKey(
        Area,
        related_name='categories'
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        area = Area.objects.get(id=self.area_id)
        return u"%s > %s" % (area.name, self.name)


class Subject(CatalogueMixin):
    """
    Subject that belongs to each area.
    """
    category = models.ForeignKey(
        Category,
        related_name='subjects',
        default=1
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        category = Category.objects.get(id=self.category_id)
        return u"%s > %s" % (category.name, self.name)


class Post(CatalogueMixin):
    """
    Main model of the application, is essentially information of a subject.
    """
    subject = models.ForeignKey(
        Subject,
        related_name='posts'
    )
    resume = models.CharField(
        max_length=150
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        verbose_name='author'
    )
    available_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name=u'available_posts',
        verbose_name='users who can view the post.'
    )
    editable_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name=u'editable_posts',
        verbose_name='users who can edit the post.'
    )
