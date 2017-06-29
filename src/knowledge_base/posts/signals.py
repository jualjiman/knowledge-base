# -*- coding: utf-8 -*-
from django.core.cache import cache

from knowledge_base.posts.search_indexes import PostIndex
from knowledge_base.utils.decorators import skip_signal


@skip_signal()
def clear_cache_at_saving(sender, instance, *args, **kwargs):
    """
    Updates the area information from cache.
    """
    cache.clear()


@skip_signal()
def save_post_index(sender, instance, *args, **kwargs):
    """
    Updates the information of the given Post, from the index.
    """
    med_index = PostIndex()
    med_index.update_object(instance)
    cache.clear()


@skip_signal()
def remove_post_index(sender, instance, *args, **kwargs):
    """
    Removes the information of the given Post, from the index.
    """
    med_index = PostIndex()
    med_index.remove_object(instance)
    cache.clear()
