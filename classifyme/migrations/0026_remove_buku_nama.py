# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 05:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0025_buku_nama'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buku',
            name='nama',
        ),
    ]