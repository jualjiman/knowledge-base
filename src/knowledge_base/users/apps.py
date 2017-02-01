# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

from knowledge_base.utils.signals import generate_thumbnail


class UsersAppConfig(AppConfig):
    """
    AppConfig for the ```knowledge_base.users``` module.
    """
    name = 'knowledge_base.users'

    def ready(self):
        super(UsersAppConfig, self).ready()

        model = self.get_model('User')
        post_save.connect(
            generate_thumbnail,
            sender=model
        )
