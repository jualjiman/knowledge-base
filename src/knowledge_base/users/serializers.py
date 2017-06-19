# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import serializers

from knowledge_base.core.api.serializers import ModelSerializer


class SearchUserSerializer(ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'name',
           'email',
           'text',
        )

    def get_text(self, instance):
        return instance.email


class ProfileURISerializer(ModelSerializer):
    custom_base_name = 'me'
    custom_lookup_fields = {}

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'name',
           'email',
           'thumbnail',
           'resource_uri',
        )


class ProfileSerializer(ModelSerializer):
    # To avoid cross importation.
    from knowledge_base.posts.serializers import (
        AreaURISerializer,
        SubjectURISerializer
    )

    area = AreaURISerializer()
    favorite_subjects = SubjectURISerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'email',
           'name',
           'description',
           'thumbnail',
           'area',
           'favorite_subjects',
           'can_contribute',
           'is_notificable_by_area',
        )


class ProfileUpdateSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'email',
           'name',
           'description',
           'area',
           'is_notificable_by_area',
        )


class ProfileUpdateImageSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('photo', )

    def validate(self, data):
        if 'photo' not in data:
            raise serializers.ValidationError("photo is a required field.")

        return data

    def update(self, instance, validated_data):
        instance.photo = validated_data['photo']
        instance.save()

        return instance
