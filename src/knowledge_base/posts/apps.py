# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

from knowledge_base.utils.signals import generate_thumbnail


class PostsAppConfig(AppConfig):
    """
    AppConfig for the ```knowledge_base.posts``` module.
    """
    name = 'knowledge_base.posts'

    def ready(self):
        super(PostsAppConfig, self).ready()

        model = self.get_model('Area')
        post_save.connect(
            generate_thumbnail,
            sender=model
        )
