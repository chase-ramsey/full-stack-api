# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_api', '0006_auto_20160919_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='image',
        ),
        migrations.AddField(
            model_name='review',
            name='image_url',
            field=models.CharField(default='https://firebasestorage.googleapis.com/v0/b/full-stack-images.appspot.com/o/file-media.svg?alt=media&token=8bb8a118-f9b4-422b-a8fc-9974eb8094de', max_length=150),
        ),
        migrations.AddField(
            model_name='userimage',
            name='image_url',
            field=models.CharField(default='https://firebasestorage.googleapis.com/v0/b/full-stack-images.appspot.com/o/person.svg?alt=media&token=51e701f8-817f-4b7e-a79e-353e7561ec36', max_length=150),
        ),
    ]
