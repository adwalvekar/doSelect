# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('token', models.CharField(max_length=20)),
                ('orignal_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('compressed_name', models.CharField(max_length=100, unique=True)),
                ('path', models.CharField(max_length=250)),
                ('compression_ratio', models.FloatField(default=0.0)),
            ],
        ),
    ]
