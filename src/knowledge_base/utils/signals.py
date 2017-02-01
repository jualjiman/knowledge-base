# -*- coding: utf-8 -*-
from knowledge_base.utils.decorators import skip_signal
from knowledge_base.utils.string_representations import make_slug
from knowledge_base.utils.thumbnails import make_thumbnail


@skip_signal()
def generate_slug(sender, instance, created, **kwargs):
    """
    Generates a slug for every given instance.
    """
    instance.slug = make_slug(instance, 'name')
    instance.skip_signal = True
    instance.save()


@skip_signal()
def generate_thumbnail(sender, instance, created, *args, **kwargs):
    """
    Generates a thumbnail, with the given values that should be configurated in
    thumbnail_settings property of the desired model.

    the format of this settings should be as follows (for example):

    @property
    def thumbnail_settings(self)
        return {
            "dimension": "100x100",
            "original_field": "image",
            "thumbnail_field": "thumbnail"
        }
    """
    thumbnail_settings = instance.thumbnail_settings

    original_field = getattr(
        instance,
        thumbnail_settings.get('original_field')
    )

    if original_field:
        make_thumbnail(
            instance,
            thumbnail_settings.get('original_field'),
            thumbnail_settings.get('thumbnail_field'),
            thumbnail_settings.get('dimension')
        )

    instance.skip_signal = True
    instance.save()

    del instance.skip_signal
