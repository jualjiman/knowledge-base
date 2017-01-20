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


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'author',
        'is_active'
    )

    search_fields = (
        'name',
        'subject'
    )

admin.site.register(Area, AreaAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Post, PostAdmin)
