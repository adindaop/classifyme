from django import forms
from .models import Buku

class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ('penulis', 'judul', 'penerbit', 'tahun_terbit', 'training_set_positif', 'training_set_negatif', 'testing_set')
