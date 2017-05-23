from django.db import models
from .validators import validate_file_extension
import datetime

class TrainingSetPos(models.Model):
    nama = models.CharField(max_length=100, null=True)
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/', validators=[validate_file_extension])

    def __str__(self):
        return self.nama

class TrainingSetNeg(models.Model):
    nama = models.CharField(max_length=100, null=True)
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/', validators=[validate_file_extension])

    def __str__(self):
        return self.nama

class Buku(models.Model):
    tahun_choices = []
    for y in range(1990, (datetime.datetime.now().year+5)):
        tahun_choices.append((y, y))

    penulis = models.CharField(max_length=20)
    judul = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=30)
    tahun_terbit = models.IntegerField(choices=tahun_choices, default=datetime.datetime.now().year)
    training_set_positif = models.ForeignKey(TrainingSetPos, null=True)
    training_set_negatif = models.ForeignKey(TrainingSetNeg, null=True)
    testing_set = models.FileField(null=True, upload_to='files/%Y/%m/%d/', validators=[validate_file_extension])
    priors_pos = models.FloatField(blank=True, null=True)
    priors_neg = models.FloatField(blank=True, null=True)
    hasil_pos = models.FloatField(blank=True, null=True)
    hasil_neg = models.FloatField(blank=True, null=True)
    hasil_klasifikasi = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.judul
