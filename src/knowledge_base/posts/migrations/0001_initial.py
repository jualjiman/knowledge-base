# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-22 21:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import knowledge_base.posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='last modified')),
                ('name', models.CharField(max_length=600, verbose_name=b'name')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is active')),
                ('description', models.TextField(max_length=250)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=knowledge_base.posts.models.get_area_image_path)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=knowledge_base.posts.models.get_area_thumbnail_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='last modified')),
                ('name', models.CharField(max_length=600, verbose_name=b'name')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is active')),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name=b'author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='last modified')),
                ('name', models.CharField(max_length=600, verbose_name=b'name')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is active')),
                ('description', models.TextField(max_length=250)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='posts.Area')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.Subject'),
        ),
    ]
