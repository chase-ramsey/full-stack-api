# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='owner',
        ),
    ]
