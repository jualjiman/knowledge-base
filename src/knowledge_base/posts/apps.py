# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save

from knowledge_base.utils.signals import generate_thumbnail


class PostsAppConfig(AppConfig):
    """
    AppConfig for the ```knowledge_base.posts``` module.
    """
    name = 'knowledge_base.posts'

    def ready(self):
        from knowledge_base.posts import signals
        super(PostsAppConfig, self).ready()

        model = self.get_model('Area')
        post_save.connect(
            generate_thumbnail,
            sender=model
        )

        #
        # Index signals.
        #
        model = self.get_model('Post')
        post_save.connect(
            signals.save_post_index,
            sender=model
        )

        post_delete.connect(
            signals.remove_post_index,
            sender=model
        )
