import csv
from django.shortcuts import render, get_object_or_404
from .forms import BukuForm
from .models import Buku
from django.shortcuts import redirect
from nltk.tokenize import word_tokenize


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
    context['judul'] = selected_buku

    print(selected_buku.ulasan)

    ulasan = ''
    with open('media/{}'.format(selected_buku.ulasan)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            ulasan += row['Review']
    context['ulasan'] = ulasan
    return render(request, 'classifyme/textmining.html', context)

def klasifikasi(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['judul'] = selected_buku
    return render(request, 'classifyme/klasifikasi.html', context)

def hasil(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['judul'] = selected_buku
    return render(request, 'classifyme/hasil.html', context)
