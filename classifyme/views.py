import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BukuForm, AkunForm
from .models import Buku, Akun
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

def admin(request):
    return render(request, admin.site.urls, {})

def home(request):
    return render(request, 'classifyme/home.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        akun = AkunForm(request.POST)
        if akun.is_valid():
            akun = akun.save()
            registered = True
        else:
            print(akun.errors)
    else:
        akun = AkunForm()
    return render(request, 'classifyme/register.html', {'akun': akun, 'registered': registered})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('nama_pengguna')
        password = request.POST.get('kata_sandi')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                return HttpResponseRedirect('/classifyme/')
            else:
                return HttpResponse("Akun tidak terdaftar.")
        else:
            return HttpResponse("Nama pengguna dan kata sandi tidak sesuai.")
    else:
        return render(request, 'classifyme/login.html', {})

def input(request):
    if request.method == 'POST':
        buku = BukuForm(request.POST, request.FILES)
        if buku.is_valid():
            buku.save()
            return redirect('classifyme:data')
    else:
        form = BukuForm()
    return render(request, 'classifyme/input.html', {'form': form})

def data(request):
    context = {}
    buku_query = Buku.objects.all()
    context['buku'] = buku_query
    return render(request, 'classifyme/data.html', context)

def textmining(request, buku_id):
    buku = get_object_or_404(Buku, id=buku_id)
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku

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
    context['buku'] = selected_buku

    ulasan = ''
    with open('media/{}'.format(selected_buku.ulasan)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            ulasan += row['Review']

    case_folding = ulasan.lower()
    tokenized_words = word_tokenize(case_folding)

    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence = []
    for w in tokenized_words:
        if w not in stop_words:
            filtered_sentence.append(w)

    word_list = set(stopwords.words("adjektiva"))
    filtered_word = []
    for a in tokenized_words:
        if a in word_list:
            filtered_word.append(a)

    # bigrams = list(ngrams(filtered_word,2))
    context['filtered_word'] = filtered_word

    return render(request, 'classifyme/klasifikasi.html', context)

def hasil(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku
    return render(request, 'classifyme/hasil.html', context)
