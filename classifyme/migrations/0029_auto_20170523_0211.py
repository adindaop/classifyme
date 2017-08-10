# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 02:11
from __future__ import unicode_literals

import classifyme.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifyme', '0028_auto_20170501_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buku',
            name='testing_set',
            field=models.FileField(null=True, upload_to='files/%Y/%m/%d/', validators=[classifyme.validators.validate_file_extension]),
        ),
    ]
