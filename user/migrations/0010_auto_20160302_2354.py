# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_housemate_boetes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housemate',
            old_name='boetes',
            new_name='boetes_open',
        ),
        migrations.AddField(
            model_name='housemate',
            name='boetes_sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='housemate',
            name='boetes_total',
            field=models.IntegerField(default=0),
        ),
    ]
