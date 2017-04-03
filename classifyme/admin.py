from django.contrib import admin
from .models import Buku, Klasifikasi, Akun

class AkunAdmin(admin.ModelAdmin):
    list_display = ['nama_pengguna', 'email', 'nama_depan', 'nama_belakang']
    search_fields = ['nama_pengguna']
    list_per_page = 20
admin.site.register(Akun,AkunAdmin)

class BukuAdmin(admin.ModelAdmin):
    list_display = ['penulis', 'judul', 'penerbit', 'tahun_terbit', 'ulasan']
    list_filter = ('penulis', 'tahun_terbit')
    search_fields = ['penulis', 'judul']
    list_per_page = 20

admin.site.register(Buku,BukuAdmin)

class KlasifikasiAdmin(admin.ModelAdmin):
    list_display = ['judul', 'hasil_klasifikasi']
    list_filter = ('hasil_klasifikasi',)
    search_fields = ['judul', 'hasil_klasifikasi']
    list_per_page = 20
admin.site.register(Klasifikasi,KlasifikasiAdmin)
