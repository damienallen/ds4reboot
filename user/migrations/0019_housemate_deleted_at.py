# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-05-14 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20161113_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemate',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
