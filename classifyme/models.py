from django.db import models

class TrainingSetPos(models.Model):
    nama = models.CharField(max_length=100, null=True)
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')

    def __str__(self):
        return self.nama

class TrainingSetNeg(models.Model):
    nama = models.CharField(max_length=100, null=True)
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')

    def __str__(self):
        return self.nama

class Buku(models.Model):
    penulis = models.CharField(max_length=20)
    judul = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=30)
    tahun_terbit = models.CharField(max_length=4)
    training_set_positif = models.ForeignKey(TrainingSetPos, null=True)
    training_set_negatif = models.ForeignKey(TrainingSetNeg, null=True)
    testing_set = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')
    priors_pos = models.FloatField(blank=True, null=True)
    priors_neg = models.FloatField(blank=True, null=True)
    hasil_pos = models.FloatField(blank=True, null=True)
    hasil_neg = models.FloatField(blank=True, null=True)
    hasil_klasifikasi = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.judul
