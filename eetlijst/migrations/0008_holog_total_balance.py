# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-13 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eetlijst', '0007_userlist_list_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='holog',
            name='total_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
