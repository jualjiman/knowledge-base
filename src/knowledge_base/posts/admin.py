# -*- coding: utf-8 -*-
from django.contrib import admin

from knowledge_base.posts.models import Area, Category, Post, Subject


class AreaAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'is_active'
    )

    search_fields = (
        'name',
        'description'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'area',
        'is_active'
    )

    search_fields = (
        'name',
        'description'
    )

    list_filter = ('area', )


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        '_category',
        'area',
        'is_active'
    )

    search_fields = (
        'name',
        'description'
    )

    list_filter = (
        'category',
        'category__area',
    )

    def _category(self, instance):
        return instance.category.name.encode('utf-8')


    def area(self, instance):
        return instance.category.area.name.encode('utf-8')


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        '_subject',
        '_category',
        'area',
        'author',
        'is_active'
    )

    list_filter = (
        'subject__category__area',
        'subject__category',
        'subject',
    )

    search_fields = (
        'category'
        'subject',
        'name',
    )

    def _subject(self, instance):
        return instance.subject.name.encode('utf-8')

    def _category(self, instance):
        return instance.subject.category.name.encode('utf-8')

    def area(self, instance):
        return instance.subject.category.area.name.encode('utf-8')


admin.site.register(Area, AreaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Post, PostAdmin)
