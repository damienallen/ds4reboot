# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 23:31
from __future__ import unicode_literals

import annoying.fields
from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bierlijst', '0002_auto_20160301_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summation',
            name='user',
            field=annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
