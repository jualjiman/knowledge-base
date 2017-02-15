# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import serializers

from knowledge_base.core.api.serializers import ModelSerializer


class ProfileURISerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'name',
           'last_name',
           'email',
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
           'last_name',
           'description',
           'thumbnail',
           'area',
           'favorite_subjects',
        )


class ProfileUpdateSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'email',
           'name',
           'last_name',
           'description',
           'area',
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
