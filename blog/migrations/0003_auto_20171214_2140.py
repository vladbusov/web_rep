# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171214_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.UserProfile', verbose_name='пользователь'),
            preserve_default=False,
        ),
    ]
