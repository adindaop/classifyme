# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('penulis', models.CharField(max_length=20)),
                ('judul', models.CharField(max_length=100)),
                ('penerbit', models.CharField(max_length=30)),
                ('tahun_terbit', models.CharField(max_length=4)),
                ('input_ulasan', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hasil_klasifikasi', models.CharField(max_length=7)),
                ('buku', models.ForeignKey(to='classifyme.Book')),
            ],
        ),
    ]
