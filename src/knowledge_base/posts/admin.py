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
        'category',
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

    def area(self, instance):
        return instance.category.area.name


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'category',
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

    def category(self, instance):
        return instance.subject.category.name

    def area(self, instance):
        return instance.subject.category.area.name


admin.site.register(Area, AreaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Post, PostAdmin)
