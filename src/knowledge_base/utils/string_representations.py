# -*- coding: utf-8 -*-
from django.utils.text import slugify


def make_slug(obj, original_field):
    original_name = getattr(obj, original_field)
    slug = slugify(original_name)
    return slug
