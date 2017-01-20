# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from knowledge_base.core.api.serializers import ModelSerializer
from knowledge_base.posts.serializers import AreaSerializer, SubjectSerializer


class UserSerializer(ModelSerializer):
    favorite_subjects = SubjectSerializer(many=True)
    area = AreaSerializer()

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
