# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 18:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='текст ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='верный?')),
                ('rating_num', models.IntegerField(default=0, verbose_name='рейтинг')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='дата и время добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Question', verbose_name='связанный вопрос')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='верный')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Answer', verbose_name='оцененный ответ')),
                ('voted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='оценено пользователем')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='верный')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Question', verbose_name='оцененный вопрос')),
                ('voted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='оценено пользователем')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='аватар')),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='дата регистрации')),
                ('rating', models.IntegerField(blank=True, default=0, verbose_name='рейтинг')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together=set([('question', 'voted_by')]),
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together=set([('answer', 'voted_by')]),
        ),
    ]
