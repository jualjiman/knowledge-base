# -*- coding: utf-8 -*-
from haystack import indexes

from knowledge_base.posts.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    post_id = indexes.CharField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    resume = indexes.CharField(model_attr='resume')
    content = indexes.CharField(model_attr='content')
    author = indexes.CharField(model_attr='author__name')
    author_id = indexes.IntegerField(model_attr='author__id')
    subject = indexes.CharField(model_attr='subject__name')
    available_to = indexes.MultiValueField()

    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Post

    def prepare_available_to(self, obj):
        return [
            user.id
            for user in obj.available_to.all()
        ]

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
