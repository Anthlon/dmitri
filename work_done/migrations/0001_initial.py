# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDoneImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='work_done/detail', verbose_name='Дополнительное изображение')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDoneModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Полное содержание')),
                ('add_dt', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('image', models.ImageField(upload_to='work_done/avatar', verbose_name='Основное изображение')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Пример завершенной работы',
                'verbose_name_plural': 'Примеры завершенных работ',
                'ordering': ['-add_dt'],
            },
        ),
        migrations.AddField(
            model_name='workdoneimage',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_done.WorkDoneModel'),
        ),
    ]
