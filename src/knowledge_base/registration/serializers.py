# -*- coding: utf-8 -*-
import hashlib
import random

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from rest_framework import serializers

from knowledge_base.utils.refresh_token import create_token


class RegistrationProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
            'email',
            'password',
            'photo',
        )

    def create(self, validated_data):
        #
        # Getting url schema from request meta data.
        #
        request = self.context['request']
        url_schema = request.META['wsgi.url_scheme']

        user_model = get_user_model()

        user = user_model(**validated_data)
        user.set_password(user.password)
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        email = user.email

        if isinstance(email, unicode):
            email = email.encode('utf-8')

        key = hashlib.sha1(salt + email).hexdigest()
        user.activation_code = key
        user.save()

        current_site = Site.objects.get_current()
        url = '{0}://{1}/activate/{2}'.format(
            url_schema,
            current_site.domain,
            key
        )

        # Constructs the context to be passed to the renderer.
        context = {
            'activation_link': url,
            'user_full_name': user.get_full_name()
        }
        # Renders the plain text message.
        message_text = render_to_string(
            'users/email/confirmation.txt',
            context
        )
        # Renders the html message.
        message_html = render_to_string(
            'users/email/confirmation.html',
            context
        )
        # Send a mail with the data for account activation
        user.send_email(
            _('Activa tu cuenta'),
            message_text,
            message_html
        )

        return user


class RegistrationResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'thumbnail',
            'name',
            'email',
            'token'
        )

    def get_token(self, obj):
        """
        Create token to user when user register.
        """
        return create_token(obj)
