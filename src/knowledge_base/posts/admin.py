# -*- coding: utf-8 -*-
from django.contrib import admin

from knowledge_base.posts.models import Area, Post, Subject


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


class SubjectAdmin(admin.ModelAdmin):
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


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'area',
        'author',
        'is_active'
    )

    list_filter = (
        'subject__area',
        'subject',
    )

    search_fields = (
        'name',
        'subject'
    )

    def area(self, instance):
        return instance.subject.area.name

admin.site.register(Area, AreaAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Post, PostAdmin)
