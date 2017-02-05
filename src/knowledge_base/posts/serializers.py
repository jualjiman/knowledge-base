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


class AreaResumeSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'resource_uri'
        )


class SubjectSerializer(ModelSerializer):
    area = AreaResumeSerializer()

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'description',
            'area',
        )


class SubjectResumeSerializer(ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'resource_uri',
        )


class PostSerializer(ModelSerializer):
    # To avoid cross importation.
    # from knowledge_base.users.serializers import ProfileResumeSerializer
    #
    # subject = SubjectResumeSerializer()
    # author = ProfileResumeSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'content',
            'author',
            'subject',
        )


class PostResumeSerializer(ModelSerializer):

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
