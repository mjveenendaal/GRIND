# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 12:52
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grind', '0004_auto_20170613_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='point_cloud',
            name='xyzpoint',
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=28992),
        ),
    ]
