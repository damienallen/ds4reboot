# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20160306_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemate',
            name='allergies',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
