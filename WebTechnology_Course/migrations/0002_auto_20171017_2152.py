# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 14:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WebTechnology_Course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='uploaded_by_user',
        ),
        migrations.AddField(
            model_name='book',
            name='last_update',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.ManyToManyField(related_name='Rating', to='WebTechnology_Course.BookRating'),
        ),
        migrations.AddField(
            model_name='book',
            name='upload_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='book',
            name='uploaded_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
    ]