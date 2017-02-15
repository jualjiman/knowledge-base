# -*- coding: utf-8 -*-
from knowledge_base.core.api.serializers import ModelSerializer
from knowledge_base.posts.models import Area, Post, Subject


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
    class Meta:
        model = Area
        fields = (
            'id',
            'name',
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

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'resource_uri',
        )


class PostSerializer(ModelSerializer):
    # To avoid cross importation.
    # from knowledge_base.users.serializers import ProfileURISerializer
    #
    # subject = SubjectURISerializer()
    # author = ProfileURISerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'content',
            'author',
            'subject',
        )


class PostURISerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'resource_uri',
        )


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'content',
            'author',
            'subject',
        )


class PostDocSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'content',
            'subject',
        )
