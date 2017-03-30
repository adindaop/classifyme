from django.shortcuts import render, get_object_or_404
from .forms import BukuForm
from .models import Buku
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def admin(request):
    return render(request, admin.site.urls, {})

def home(request):
    return render(request, 'classifyme/home.html', {})

def input(request):
    context = {} #inisialisasi harus kosong
    buku_query = Buku.objects.all() #questions_query = variabel
    context['buku'] = buku_query #yg di tanda '' boleh beda dr variabel
    return render(request, 'classifyme/input.html', context)

def textmining(request, buku_id):
    buku = get_object_or_404(Buku, id=buku_id)
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['judul', 'ulasan'] = selected_buku
    return render(request, 'classifyme/textmining.html', context)
