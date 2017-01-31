# -*- coding: utf-8 -*-
from rest_framework import serializers

from knowledge_base.users.models import User
from knowledge_base.utils.refresh_token import create_token


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        required=True
    )

    def validate(self, data):
        """
        Validation email, password and active status
        """
        try:
            user = User.objects.get(email__iexact=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid credentials")

        if not user.check_password(data.get('password')):
            raise serializers.ValidationError("invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError(
                'the user has not been activated'
            )

        return data

    def get_user(self, data):
        """
        return user object
        """
        return User.objects.get(email__iexact=data.get('email'))


class LoginResponseSerializer(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('token', )

    def get_token(self, obj):
        """
        Create token.
        """
        return create_token(obj)
