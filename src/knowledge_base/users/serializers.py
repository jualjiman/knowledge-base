# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import serializers

from knowledge_base.core.api.serializers import ModelSerializer


class ProfileSerializer(ModelSerializer):
    # To avoid cross importation.
    from knowledge_base.posts.serializers import (
        AreaResumeSerializer,
        SubjectResumeSerializer
    )

    area = AreaResumeSerializer()
    favorite_subjects = SubjectResumeSerializer(many=True)

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


class ProfileResumeSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
           'id',
           'name',
           'last_name',
           'email',
           'resource_uri',
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
