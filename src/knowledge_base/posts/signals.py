# -*- coding: utf-8 -*-
from django.core.cache import cache

from knowledge_base.posts.search_indexes import PostIndex
from knowledge_base.utils.decorators import skip_signal

from knowledge_base.posts.tasks import notificate_users_new_post


@skip_signal()
def clear_cache_at_saving(sender, instance, *args, **kwargs):
    """
    Updates the area information from cache.
    """
    cache.clear()


@skip_signal()
def save_post_index(sender, instance, created, *args, **kwargs):
    """
    Updates the information of the given Post, from the index,
    clears the cache to give updated information and
    sends an email to all registered users (only if creating)
    """
    med_index = PostIndex()
    med_index.update_object(instance)

    cache.clear()

    # If is a new post, send an email to all those users that want to be
    # notified.
    if created:
        notificate_users_new_post.apply_async((instance,))


@skip_signal()
def remove_post_index(sender, instance, *args, **kwargs):
    """
    Removes the information of the given Post, from the index.
    """
    med_index = PostIndex()
    med_index.remove_object(instance)
    cache.clear()
