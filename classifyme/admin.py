from django.contrib import admin
from .models import TrainingSetPos, TrainingSetNeg, Buku

class TrainingSetPosAdmin(admin.ModelAdmin):
    list_display = ['nama', 'file']
admin.site.register(TrainingSetPos,TrainingSetPosAdmin)

class TrainingSetNegAdmin(admin.ModelAdmin):
    list_display = ['nama', 'file']
admin.site.register(TrainingSetNeg,TrainingSetNegAdmin)

class BukuAdmin(admin.ModelAdmin):
    exclude = ['priors_pos', 'priors_neg', 'hasil_pos', 'hasil_neg', 'hasil_preprocessing_pos', 'hasil_preprocessing_neg']
    list_display = ['penulis', 'judul', 'penerbit', 'tahun_terbit', 'training_set_positif', 'training_set_negatif', 'testing_set', 'hasil_klasifikasi']
    list_filter = ('penulis', 'tahun_terbit')
    search_fields = ['penulis', 'judul']
    list_per_page = 20
admin.site.register(Buku,BukuAdmin)
