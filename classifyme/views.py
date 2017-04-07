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
import collections

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

    # context['tokenized_words_positif'] = tokenized_words_positif

    word_list = set(stopwords.words("adjektiva"))
    filtered_word_positif = []
    for a in filtered_sentence_positif:
        if a in word_list:
            filtered_word_positif.append(a)

    # bigrams = list(ngrams(filtered_word,2))
    context['filtered_word_positif'] = filtered_word_positif

    # count(positif) / (untuk FreqDist's total outcomes)
    jumlah_kata_positif = len(filtered_word_positif)
    context['jumlah_kata_positif'] = jumlah_kata_positif

    # FreqDist's total samples
    wordfreq_positif = nltk.FreqDist(filtered_word_positif)
    wordfreq_sample_positif = 0
    for sample in wordfreq_positif:
        wordfreq_sample_positif += 1
        print('wordfreq_sample_positif', wordfreq_sample_positif)
    context['wordfreq_sample_positif'] = wordfreq_sample_positif

    #count(w,positif)
    # word_counts = collections.Counter(filtered_word_positif)
    # wordfreq_positif_list = ''
    # for word, count in sorted(word_counts.items()):
    #     wordfreq_positif_list += '"%s" = %d\n' % (word, count)
    # context['wordfreq_positif_list'] = wordfreq_positif_list


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

    # count(negatif) / (untuk FreqDist's total outcomes)
    jumlah_kata_negatif = len(filtered_word_negatif)
    context['jumlah_kata_negatif'] = jumlah_kata_negatif

    # untuk FreqDist's total samples
    wordfreq_negatif = nltk.FreqDist(filtered_word_negatif)
    wordfreq_sample_negatif = 0
    for sample in wordfreq_negatif:
        wordfreq_sample_negatif += 1
    context['wordfreq_sample_negatif'] = wordfreq_sample_negatif

    # untuk (samples, outcomes)'s list
    # wordfreq_negatif_list = wordfreq_negatif.most_common()
    # context['wordfreq_negatif_list'] = wordfreq_negatif_list

    # unique words lists
    unique_words = filtered_word_positif + filtered_word_negatif
    unique_wordfreq_total = nltk.FreqDist(unique_words)
    total_unique_words = unique_wordfreq_total.most_common()
    context['total_unique_words'] = total_unique_words

    # |V| / jumlah kata unik seluruh data percobaan
    unique_wordfreq_total = nltk.FreqDist(unique_words)
    wordfreq_sample_total = 0
    for sample in unique_wordfreq_total:
        wordfreq_sample_total += 1
    context['wordfreq_sample_total'] = wordfreq_sample_total

    ulasan_testing = ''
    with open('media/{}'.format(selected_buku.ulasan_testing)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            ulasan_testing += row['Review']

    case_folding = ulasan_testing.lower()
    tokenized_words_testing = word_tokenize(case_folding)

    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_testing = []
    for w in tokenized_words_testing:
        if w not in stop_words:
            filtered_sentence_testing.append(w)

    # context['tokenized_words_positif'] = tokenized_words_positif

    word_list = set(stopwords.words("adjektiva"))
    filtered_word_testing = []
    for a in filtered_sentence_testing:
        if a in word_list:
            filtered_word_testing.append(a)

    # bigrams = list(ngrams(filtered_word,2))
    context['filtered_word_testing'] = filtered_word_testing

    # kata dalam data testing yang muncul di kelas positif DAN negatif
    list_dua_dua = []
    for elem in filtered_word_testing:
        if elem in filtered_word_positif and elem in filtered_word_negatif:
            if elem not in list_dua_dua:
                list_dua_dua.append(elem)
    context['list_dua_dua'] = list_dua_dua

    # count(w, positif)
    word_counts = collections.Counter(filtered_word_positif)
    wordfreq_positif_list = ''
    for w, c in sorted(word_counts.items()):
        if w in list_dua_dua:
            wordfreq_positif_list += '"%s" = %d\n' % (w, c)
    context['wordfreq_positif_list'] = wordfreq_positif_list

    # count(w,positif) + 1
    word_counts = collections.Counter(filtered_word_positif)
    wordfreq_positif_list_plus = ''
    for w, c in sorted(word_counts.items()):
        if w in list_dua_dua:
            wordfreq_positif_list_plus += '"%s" = %d\n' % (w, c+1)
    context['wordfreq_positif_list_plus'] = wordfreq_positif_list_plus

    # count(w,negatif)
    word_counts = collections.Counter(filtered_word_negatif)
    wordfreq_negatif_list = ''
    for w, c in sorted(word_counts.items()):
        if w in list_dua_dua:
            wordfreq_negatif_list += '"%s" = %d\n' % (w, c)
    context['wordfreq_negatif_list'] = wordfreq_negatif_list

    # count(w,negatif) + 1
    word_counts = collections.Counter(filtered_word_negatif)
    wordfreq_negatif_list_plus = ''
    for w, c in sorted(word_counts.items()):
        if w in list_dua_dua:
            wordfreq_negatif_list_plus += '"%s" = %d\n' % (w, c+1)
    context['wordfreq_negatif_list_plus'] = wordfreq_negatif_list_plus

    # word_counts = collections.Counter(filtered_word_positif)
    # cp_pembilang = ''
    # for w, c in sorted(word_counts.items()):
    #     cp_pembilang = int(c+1)
    #     if w in list_dua_dua:
    #         cp_pembilang += '"%s" = %d\n' % (w, cp_pembilang)
    # context['cp_pembilang'] = cp_pembilang

    coba = float(jumlah_kata_positif + wordfreq_sample_total)
    context['coba'] = coba

    # conditional probabilities positif
    word_counts = collections.Counter(filtered_word_positif)
    cp_pos = ''
    for w, c in sorted(word_counts.items()):
        cp_pembilang = c+1
        cp_penyebut = jumlah_kata_positif + wordfreq_sample_total
        cp = float(cp_pembilang/cp_penyebut)
        if w in list_dua_dua:
            cp_pos += '"{}" = {}\n'.format(w, cp)
            # cp_pos += '"%s" = %f\n' % (w, cp) -> ini kalau cuma mau nampilin bbrp angka di belakang koma (ga lengkap)
    context['cp_pos'] = cp_pos

    # conditional probabilities negatif
    word_counts = collections.Counter(filtered_word_negatif)
    cp_neg = ''
    for w, c in sorted(word_counts.items()):
        cp_pembilang = c+1
        cp_penyebut = jumlah_kata_negatif + wordfreq_sample_total
        cp = float(cp_pembilang/cp_penyebut)
        if w in list_dua_dua:
            cp_neg += '"{}" = {}\n'.format(w, cp)
    context['cp_neg'] = cp_neg

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

# jumlah kejadian kata w dalam kelas positif + 1
# frequency_list = []
# for q in filtered_word_positif:
#     frequency_list.append(filtered_word_positif.count(q))
# context['frequency_list'] = frequency_list
# frequency_list_plus = [x+1 for x in frequency_list]
# context['frequency_list_plus'] = frequency_list_plus

# pairs for [filtered_word_positif, frequency_list_plus] + 1
# pairs = str(list(zip(filtered_word_positif, frequency_list_plus)))
# context['pairs'] = pairs

# jumlah kejadian kata w dalam kelas positif
# wordfreq = []
# for w in filtered_word_positif:
#     wordfreq.append(filtered_word_positif.count(w))
# frequency_positif = str(wordfreq)
# frequency_word_positif = str(list(zip(filtered_word_positif, wordfreq)))
# context['frequency_word_positif'] = frequency_word_positif
