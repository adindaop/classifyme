from django.db import models

class Buku(models.Model):
    penulis = models.CharField(max_length=20)
    judul = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=30)
    tahun_terbit = models.CharField(max_length=4)
    ulasan = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.judul

class Klasifikasi(models.Model):
    judul = models.ForeignKey(Buku)
    hasil_klasifikasi = models.CharField(max_length=7)

    def __str__(self):
        return self.judul
