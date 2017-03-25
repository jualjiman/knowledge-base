# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from drf_haystack import serializers as haystack_serializers

from rest_framework import serializers

from knowledge_base.core.api.serializers import ModelSerializer
from knowledge_base.posts.models import Area, Post, Subject
from knowledge_base.posts.search_indexes import PostIndex


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'description',
            'thumbnail',
        )


class AreaURISerializer(ModelSerializer):
    custom_lookup_fields = {
        "pk": 'pk',
    }

    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'description',
            'thumbnail',
            'resource_uri'
        )


class SubjectSerializer(ModelSerializer):
    area = AreaURISerializer()

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'description',
            'area',
        )


class SubjectURISerializer(ModelSerializer):
    custom_lookup_fields = {
        "pk": 'pk',
        "area_pk": 'area__pk',
    }
    area = AreaURISerializer()

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'description',
            'area',
            'resource_uri',
        )


class PostSerializer(ModelSerializer):
    # To avoid cross importation.
    from knowledge_base.users.serializers import (
        ProfileURISerializer,
        SearchUserSerializer
    )

    subject = SubjectURISerializer()
    author = ProfileURISerializer()
    available_to = SearchUserSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'resume',
            'content',
            'author',
            'subject',
            'is_active',
            'created_date',
            'last_modified',
            'available_to',
        )


class PostURISerializer(ModelSerializer):
    # To avoid cross importation.
    from knowledge_base.users.serializers import ProfileURISerializer

    custom_lookup_fields = {
        "pk": 'pk',
        "subject_pk": 'subject__pk',
        "area_pk": 'subject__area__pk',
    }
    subject = SubjectURISerializer()
    author = ProfileURISerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'resume',
            'subject',
            'author',
            'resource_uri',
            'is_active',
        )


class PostCreateSerializer(ModelSerializer):
    list_available_to = serializers.ListField(
        required=False
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'resume',
            'content',
            'author',
            'subject',
            'is_active',
            'list_available_to',
        )

    def create(self, validated_data):
        list_available_to = validated_data.pop('list_available_to', None)

        instance = super(PostCreateSerializer, self).create(validated_data)

        if list_available_to:
            user_model = get_user_model()
            users = user_model.objects.filter(
                id__in=list_available_to
            )

            for user in users:
                instance.available_to.add(user)

            instance.save()

        return instance

    def update(self, instance, validated_data):
        list_available_to = validated_data.pop('list_available_to', None)

        instance = super(PostCreateSerializer, self).update(
            instance,
            validated_data
        )

        #
        # Deleting current users to save new ones.
        #
        instance.available_to.through.objects.all().delete()
        if list_available_to:
            user_model = get_user_model()
            users = user_model.objects.filter(
                id__in=list_available_to
            )

            for user in users:
                instance.available_to.add(user)

            instance.save()

        return instance


class PostDocSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'resume',
            'content',
            'subject',
            'is_active',
        )


class PostSearchSerializer(haystack_serializers.HaystackSerializer):
    id = serializers.IntegerField(source="post_id")
    author = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        index_classes = (PostIndex, )
        fields = (
            'id',
            'name',
            'resume',
            'subject',
            'author',
            'content_auto',
        )

        ignore_fields = (
            'content_auto',
        )

        field_aliases = {
            "q": "content_auto",
        }

    def get_author(self, instance):
        from knowledge_base.users.serializers import ProfileURISerializer
        author = get_user_model().objects.get(id=instance.author_id)

        return ProfileURISerializer(author).data

    def get_subject(self, instance):
        subject = Subject.objects.get(id=instance.subject_id)

        return SubjectURISerializer(subject).data
