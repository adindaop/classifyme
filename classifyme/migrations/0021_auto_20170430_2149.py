# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-30 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0020_auto_20170430_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hasil',
            name='judul',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classifyme.Buku'),
        ),
    ]