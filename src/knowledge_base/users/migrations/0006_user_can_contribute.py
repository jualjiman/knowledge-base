# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-27 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_contribute',
            field=models.BooleanField(default=False, verbose_name='can_contribute'),
        ),
    ]
