# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 07:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0014_auto_20170414_0754'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Akun',
        ),
        migrations.RemoveField(
            model_name='klasifikasi',
            name='judul',
        ),
        migrations.DeleteModel(
            name='Klasifikasi',
        ),
    ]
