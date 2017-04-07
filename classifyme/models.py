from django.db import models

class Akun(models.Model):
    nama_pengguna = models.CharField(max_length=20)
    kata_sandi = models.CharField(max_length=8)
    email = models.EmailField(max_length=30)
    nama_depan = models.CharField(max_length=10)
    nama_belakang = models.CharField(max_length=10)
    foto = models.ImageField(blank=True, upload_to='picture/')

    def __str__(self):
        return self.nama_pengguna

class Buku(models.Model):
    penulis = models.CharField(max_length=20)
    judul = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=30)
    tahun_terbit = models.CharField(max_length=4)
    ulasan_positif = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')
    ulasan_negatif = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')
    ulasan_testing = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')

    def __str__(self):
        return self.judul

class Klasifikasi(models.Model):
    judul = models.ForeignKey(Buku)
    hasil_klasifikasi = models.CharField(max_length=7)

    def __str__(self):
        return self.judul
