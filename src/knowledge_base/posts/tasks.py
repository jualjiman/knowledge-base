# -*- coding: utf-8 -*-
from celery import shared_task

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


@shared_task
def notificate_users_new_post(post):
    """
    Sends message to all users that are registered to notifications by area.
    """
    area = post.subject.category.area

    user_model = get_user_model()

    notificable_users = user_model.objects.exclude(
       id=post.author.id
    ).filter(
        is_notificable_by_area=True,
        area=area
    )

    for user in notificable_users:
        # Constructs the context to be passed to the renderer.
        context = {
            'user_full_name': user.get_full_name(),
            'user_area': user.area.name.encode('utf-8'),
            'post_title': post.name,
            'post_frontend_url': post.get_frontend_url()
        }

        # Renders the plain text message.
        message_text = render_to_string(
            'users/email/new_area_content.txt',
            context
        )

        # Renders the html message.
        message_html = render_to_string(
            'users/email/new_area_content.html',
            context
        )

        # Send a mail with the data for account activation
        user.send_email(
            _('Nuevo contenido en tu area'.decode('utf-8')),
            message_text,
            message_html
        )
