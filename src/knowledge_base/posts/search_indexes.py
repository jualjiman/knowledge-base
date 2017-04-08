# -*- coding: utf-8 -*-
from haystack import indexes

from knowledge_base.posts.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    post_id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    resume = indexes.CharField(model_attr='resume')
    content = indexes.CharField(model_attr='content')
    author_id = indexes.IntegerField(model_attr='author__id')
    subject_id = indexes.IntegerField(model_attr='subject__id')
    is_active = indexes.BooleanField(model_attr='is_active')

    available_to = indexes.MultiValueField()
    is_available_to = indexes.BooleanField()

    editable_to = indexes.MultiValueField()
    is_editable_to = indexes.BooleanField()

    subject_name = indexes.CharField(model_attr='subject__name')
    area_name = indexes.CharField(model_attr='subject__area__name')

    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Post

    def prepare_available_to(self, obj):
        return [
            user.id
            for user in obj.available_to.all()
        ]

    def prepare_is_available_to(self, obj):
        if obj.available_to.all().count() > 0:
            return True
        return False

    def prepare_editable_to(self, obj):
        return [
            user.id
            for user in obj.editable_to.all()
        ]

    def prepare_is_editable_to(self, obj):
        if obj.editable_to.all().count() > 0:
            return True
        return False

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
