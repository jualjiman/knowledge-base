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


class SubjectSerializer(ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'description',
            'area',
        )


class PostSerializer(ModelSerializer):
    # to avoid cross importation.
    from knowledge_base.users.serializers import UserSerializer

    subject = SubjectSerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'content',
            'author',
            'subject',
        )
