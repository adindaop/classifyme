import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BukuForm, AkunForm
from .models import Buku, Akun
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

def admin(request):
    return render(request, admin.site.urls, {})

def home(request):
    return render(request, 'classifyme/home.html', {})

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

    print(selected_buku.ulasan_positif)

    ulasan_positif = ''
    with open('media/{}'.format(selected_buku.ulasan_positif)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_positif = 0
        for row in csvreader:
            total_row_positif += 1
            ulasan_positif += row['Review']
            jumlah_positif = len(ulasan_positif.split())
    context['total_row_positif'] = total_row_positif
    context['ulasan_positif'] = ulasan_positif
    context['jumlah_positif'] = jumlah_positif

    print(selected_buku.ulasan_negatif)

    ulasan_negatif = ''
    with open('media/{}'.format(selected_buku.ulasan_negatif)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_negatif = 0
        for row in csvreader:
            total_row_negatif += 1
            ulasan_negatif += row['Review']
            jumlah_negatif = len(ulasan_negatif.split())
    context['total_row_negatif'] = total_row_negatif
    context['ulasan_negatif'] = ulasan_negatif
    context['jumlah_negatif'] = jumlah_negatif

    total_ulasan = total_row_positif + total_row_negatif
    context['total_ulasan'] = total_ulasan

    return render(request, 'classifyme/textmining.html', context)

def klasifikasi(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku

    ulasan_positif = ''
    with open('media/{}'.format(selected_buku.ulasan_positif)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            ulasan_positif += row['Review']

    case_folding = ulasan_positif.lower()
    tokenized_words_positif = word_tokenize(case_folding)

    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_positif = []
    for w in tokenized_words_positif:
        if w not in stop_words:
            filtered_sentence_positif.append(w)

    word_list = set(stopwords.words("adjektiva"))
    filtered_word_positif = []
    for a in filtered_sentence_positif:
        if a in word_list:
            filtered_word_positif.append(a)

    # bigrams = list(ngrams(filtered_word,2))
    context['filtered_word_positif'] = filtered_word_positif

    wordfreq_positif = nltk.FreqDist(filtered_word_positif)
    wordfreq_positif_list = wordfreq_positif.most_common()
    context['wordfreq_positif_list'] = wordfreq_positif_list
    # wordfreq = []
    # for w in filtered_word_positif:
    #     wordfreq.append(filtered_word_positif.count(w))
    # frequency_positif = str(wordfreq)
    # frequency_word_positif = str(zip(filtered_word_positif, wordfreq))
    # context['frequency_word_positif'] = frequency_word_positif

    ulasan_negatif = ''
    with open('media/{}'.format(selected_buku.ulasan_negatif)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            ulasan_negatif += row['Review']

    case_folding = ulasan_negatif.lower()
    tokenized_words_negatif = word_tokenize(case_folding)

    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_negatif = []
    for w in tokenized_words_negatif:
        if w not in stop_words:
            filtered_sentence_negatif.append(w)

    word_list = set(stopwords.words("adjektiva"))
    filtered_word_negatif = []
    for a in filtered_sentence_negatif:
        if a in word_list:
            filtered_word_negatif.append(a)

    # bigrams = list(ngrams(filtered_word,2))
    context['filtered_word_negatif'] = filtered_word_negatif

    return render(request, 'classifyme/klasifikasi.html', context)

def hasil(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku
    return render(request, 'classifyme/hasil.html', context)

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
