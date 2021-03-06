# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 15:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_opened', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_closed', models.DateTimeField()),
                ('boete_open', models.BooleanField(default=True)),
                ('boete_note', models.CharField(max_length=50)),
                ('boete_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Turf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turf_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('turf_count', models.IntegerField()),
                ('turf_type', models.CharField(max_length=10)),
                ('turf_beer', models.IntegerField()),
                ('turf_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
