from django import forms
from .models import Buku, Akun

class AkunForm(forms.ModelForm):
    kata_sandi = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Akun
        fields = ('nama_pengguna', 'kata_sandi', 'email', 'nama_depan', 'nama_belakang',)
        
class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ('penulis', 'judul', 'penerbit', 'tahun_terbit', 'ulasan',)
