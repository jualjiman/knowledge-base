# -*- coding: utf-8 -*-
import hashlib
import random

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from rest_framework import serializers

from knowledge_base.registration.models import ResetPassword
from knowledge_base.utils.refresh_token import create_token


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for change password.
    """
    password = serializers.CharField(
        max_length=150,
        required=True
    )
    token = serializers.CharField(
        max_length=40,
        required=True
    )

    def validate_token(self, value):
        """
        Validation token
        """
        try:
            status = ResetPassword.objects.get(activation_key=value)
        except ResetPassword.DoesNotExist:
            raise serializers.ValidationError(
                _("The code does not exist")
            )

        if status.is_activated:
            raise serializers.ValidationError(
                _("The code has already been used")
            )
        if status.key_expired:
            raise serializers.ValidationError(
                _("The code already expired")
            )
        return value

    def create(self, validated_data):
        """
        Change password
        """
        password = validated_data.get('password', None)
        token = validated_data.get('token', None)
        use_token = ResetPassword.objects.get(activation_key=token)
        use_token.is_activated = True
        use_token.save()
        user = get_user_model.objects.get(id=use_token.user.id)
        user.set_password(password)
        user.save()

        return user


class NewPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for reset password.
    """
    email = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            'email',
        )

    def validate_email(self, value):
        """
        Validation email
        """
        try:
            user_model = get_user_model()
            user_model.objects.get(email=value)
        except user_model.DoesNotExist:
            raise serializers.ValidationError(
                _("The email does not exist")
            )

        return value

    def create(self, validated_data):
        mail = validated_data.get('email', None)
        user = ResetPassword.objects.reset_user_password(
            email=mail,
            request=self.context['request']
        )
        return user


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
        user = super(
            RegistrationProfileSerializer,
            self
        ).create(validated_data)

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        email = user.email

        if isinstance(email, unicode):
            email = email.encode('utf-8')

        key = hashlib.sha1(salt + email).hexdigest()
        user.activation_code = key
        user.save()

        current_site = Site.objects.get_current()
        url = 'https://{0}/activate/{1}'.format(current_site, key)

        # Constructs the context to be passed to the renderer.
        context = {
            'activation_link': url,
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
            'Activa tu cuenta',
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
