import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BukuForm
from .models import Buku
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import collections
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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

    #print(selected_buku.training_set_positif)
    training_set_positif = ''
    with open('media/{}'.format(selected_buku.training_set_positif.file)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_positif = 0
        for row in csvreader:
            total_row_positif += 1
            training_set_positif += row['Review']
            # jumlah_positif = len(ulasan_positif.split()) -> jumlah kata dalam ulasan positif (raw)
    context['total_row_positif'] = total_row_positif
    context['training_set_positif'] = training_set_positif
    # context['jumlah_positif'] = jumlah_positif

    # mengubah semua kata menjadi lowercase
    case_folding_pos = training_set_positif.lower()
    context['case_folding_pos'] = case_folding_pos

    # menghilangkan imbuhan kata (try Sastrawi)
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    # hasil_stemming_pos = stemmer.stem(case_folding_pos)
    # context['hasil_stemming_pos'] = hasil_stemming_pos

    # memisahkan kalimat menjadi kata
    tokenized_words_positif = word_tokenize(case_folding_pos)
    context['tokenized_words_positif'] = tokenized_words_positif

    # menghilangkan kata yang tidak perlu
    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_positif = []
    for w in tokenized_words_positif:
        if w not in stop_words:
            filtered_sentence_positif.append(w)
    context['filtered_sentence_positif'] = filtered_sentence_positif

    # menampilkan kata ungkapan yang merujuk ke ungkapan positif dan negatif
    word_list = set(stopwords.words("wordlist"))
    filtered_word_positif = []
    for a in filtered_sentence_positif:
        if a in word_list:
            filtered_word_positif.append(a)
    context['filtered_word_positif'] = filtered_word_positif

    # count(w, training_pos)
    word_counts = collections.Counter(filtered_word_positif)
    wordfreq_positif_list = []
    for w, cp in sorted(word_counts.items()):
        wordfreq_positif_list.append({'w': w, 'cp': cp})
    context['wordfreq_positif_list'] = wordfreq_positif_list

    # save preprocessing positif result to django model field
    selected_preprocessing = Buku.objects.get(id=int(buku_id))
    selected_preprocessing.hasil_preprocessing_pos = filtered_word_positif
    selected_preprocessing.save()

    # count(positif) / (untuk FreqDist's total outcomes)
    jumlah_kata_positif = len(filtered_word_positif)
    context['jumlah_kata_positif'] = jumlah_kata_positif

    #print(selected_buku.training_set_negatif)
    training_set_negatif = ''
    with open('media/{}'.format(selected_buku.training_set_negatif.file)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_negatif = 0
        for row in csvreader:
            total_row_negatif += 1
            training_set_negatif += row['Review']
            # jumlah_negatif = len(ulasan_negatif.split()) -> jumlah kata dalam ulasan negatif (raw)
    context['total_row_negatif'] = total_row_negatif
    context['training_set_negatif'] = training_set_negatif
    # context['jumlah_negatif'] = jumlah_negatif

    # mengubah semua kata menjadi lowercase
    case_folding_neg = training_set_negatif.lower()
    context['case_folding_neg'] = case_folding_neg

    # menghilangkan imbuhan kata (try Sastrawi)
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    # hasil_stemming_neg = stemmer.stem(training_set_negatif)
    # context['hasil_stemming_neg'] = hasil_stemming_neg

    # memisahkan kalimat menjadi kata
    tokenized_words_negatif = word_tokenize(case_folding_neg)
    context['tokenized_words_negatif'] = tokenized_words_negatif

    # menghilangkan kata yang tidak perlu
    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_negatif = []
    for w in tokenized_words_negatif:
        if w not in stop_words:
            filtered_sentence_negatif.append(w)
    context['filtered_sentence_negatif'] = filtered_sentence_negatif

    # menampilkan kata ungkapan yang merujuk ke ungkapan positif dan negatif
    word_list = set(stopwords.words("wordlist"))
    filtered_word_negatif = []
    for a in filtered_sentence_negatif:
        if a in word_list:
            filtered_word_negatif.append(a)
    context['filtered_word_negatif'] = filtered_word_negatif

    # count(w, training_neg)
    word_counts = collections.Counter(filtered_word_negatif)
    wordfreq_negatif_list = []
    for w, cp in sorted(word_counts.items()):
        wordfreq_negatif_list.append({'w': w, 'cp': cp})
    context['wordfreq_negatif_list'] = wordfreq_negatif_list

    # save preprocessing negatif result to django model field
    selected_preprocessing = Buku.objects.get(id=int(buku_id))
    selected_preprocessing.hasil_preprocessing_neg = filtered_word_negatif
    selected_preprocessing.save()

    # count(negatif) / (untuk FreqDist's total outcomes)
    jumlah_kata_negatif = len(filtered_word_negatif)
    context['jumlah_kata_negatif'] = jumlah_kata_negatif

    # total ulasan
    total_ulasan = total_row_positif + total_row_negatif
    context['total_ulasan'] = total_ulasan

    # priors positif
    priors_pos = float(total_row_positif / total_ulasan)
    context['priors_pos'] = priors_pos

    # save the priors positif result to django model field
    selected_priors = Buku.objects.get(id=int(buku_id))
    selected_priors.priors_pos = priors_pos
    selected_priors.save()

    # priors negatif
    priors_neg = float(total_row_negatif / total_ulasan)
    context['priors_neg'] = priors_neg

    # save the priors negatif result to django model field
    selected_priors = Buku.objects.get(id=int(buku_id))
    selected_priors.priors_neg = priors_neg
    selected_priors.save()

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

    # print(selected_buku.testing_set)
    testing_set = ''
    with open('media/{}'.format(selected_buku.testing_set)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            testing_set += row['Review']
    context['testing_set'] = testing_set

    # mengubah semua kata menjadi lowercase
    case_folding_test = testing_set.lower()
    context['case_folding_test'] = case_folding_test

    # menghilangkan imbuhan kata (try Sastrawi)
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    # hasil_stemming_test = stemmer.stem(testing_set)
    # context['hasil_stemming_test'] = hasil_stemming_test

    # memisahkan kalimat menjadi kata
    tokenized_words_testing = word_tokenize(case_folding_test)
    context['tokenized_words_testing'] = tokenized_words_testing

    # menghilangkan kata yang tidak perlu
    stop_words = set(stopwords.words("bahasa"))
    filtered_sentence_testing = []
    for w in tokenized_words_testing:
        if w not in stop_words:
            filtered_sentence_testing.append(w)
    context['filtered_sentence_testing'] = filtered_sentence_testing

    # menampilkan kata ungkapan yang merujuk ke ungkapan positif dan negatif
    word_list = set(stopwords.words("wordlist"))
    filtered_word_testing = []
    for a in filtered_sentence_testing:
        if a in word_list:
            filtered_word_testing.append(a)
    context['filtered_word_testing'] = filtered_word_testing

    # count(w, testing)
    word_counts = collections.Counter(filtered_word_testing)
    wordfreq_testing_list = []
    for w, cp in sorted(word_counts.items()):
        wordfreq_testing_list.append({'w': w, 'cp': cp})
    context['wordfreq_testing_list'] = wordfreq_testing_list

    # count(w,positif) + 1
    wordfreq_test_in_pos = {}
    for item_testing in wordfreq_testing_list:
        for item_positif in wordfreq_positif_list:
            if item_testing['w'] == item_positif['w'] :
                cp=(item_positif['cp']+1)
                wordfreq_test_in_pos[item_testing['w']] = cp
            elif item_testing['w'] != item_positif['w'] and item_testing['w'] not in wordfreq_test_in_pos:
                wordfreq_test_in_pos[item_testing['w']] = 1
    context['wordfreq_test_in_pos'] = wordfreq_test_in_pos

    # count(w,negatif) + 1
    wordfreq_test_in_neg = {}
    for item_testing in wordfreq_testing_list:
        for item_negatif in wordfreq_negatif_list:
            if item_testing['w'] == item_negatif['w'] :
                cp = (item_negatif['cp']+1)
                wordfreq_test_in_neg[item_testing['w']] = cp
            elif item_testing['w'] != item_negatif['w'] and item_testing['w'] not in wordfreq_test_in_neg:
                wordfreq_test_in_neg[item_testing['w']] = 1
    context['wordfreq_test_in_neg'] = wordfreq_test_in_neg

    # conditional probabilities positif
    cp_pos_list = {}
    for w, cp in wordfreq_test_in_pos.items():
        cp_pembilang = cp
        cp_penyebut = jumlah_kata_positif + wordfreq_sample_total
        cp_hasil = float(cp_pembilang/cp_penyebut)
        cp_pos_list[w] = cp_hasil
    context['cp_pos_list'] = cp_pos_list

    # conditional probabilities negatif
    cp_neg_list = {}
    for w, cp in wordfreq_test_in_neg.items():
        cp_pembilang = cp
        cp_penyebut = jumlah_kata_negatif + wordfreq_sample_total
        cp_hasil = float(cp_pembilang/cp_penyebut)
        cp_neg_list[w] = cp_hasil
    context['cp_neg_list'] = cp_neg_list

    # hasil akhir positif
    product_cp_pos = 1
    cp_words_pos = {}
    i = 0
    while i < len(cp_pos_list):
        cp_words_pos.append(cp_pos_list[i]['cp'] ** wordfreq_testing_list[i]['cp']) #cp**jumlah_kata
        i += 1
    for x in cp_words_pos:
        product_cp_pos *=x #pengalian semua objek dalam list
    hasil_pos = selected_buku.priors_pos * product_cp_pos #pengalian hasil pengalian semua objek dalam list dengan priors
    context['hasil_pos'] = float(hasil_pos)

    # # save hasil akhir positif to django model field
    # selected_hasil = Buku.objects.get(id=int(buku_id))
    # selected_hasil.hasil_pos = hasil_pos
    # selected_hasil.save()

    # hasil akhir negatif
    # product_cp_neg = 1
    # cp_words_neg = []
    # i = 0
    # while i < len(cp_neg_list):
    #     cp_words_neg.append(cp_neg_list[i]['cp'] ** wordfreq_testing_list[i]['cp']) #cp**jumlah_kata
    #     i += 1
    # for x in cp_words_neg:
    #     product_cp_neg *=x #pengalian semua objek dalam list
    # hasil_neg = selected_buku.priors_neg * product_cp_neg #pengalian hasil pengalian semua objek dalam list dengan priors
    # context['hasil_neg'] = hasil_neg
    #
    # # save hasil akhir negatif to django model field
    # selected_hasil = Buku.objects.get(id=int(buku_id))
    # selected_hasil.hasil_neg = hasil_neg
    # selected_hasil.save()

    return render(request, 'classifyme/textmining.html', context)

def hasil(request, buku_id):
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku

    if selected_buku.hasil_pos > selected_buku.hasil_neg:
        hasil_akhir = "Positif"
    elif selected_buku.hasil_pos < selected_buku.hasil_neg:
        hasil_akhir = "Negatif"
    else:
        hasil_akhir = "Tidak Terdefinisi"
    context['hasil_akhir'] = hasil_akhir

    #save hasil akhir to django model field
    selected_hasil = Buku.objects.get(id=int(buku_id))
    selected_hasil.hasil_klasifikasi = hasil_akhir
    selected_hasil.save()

    return render(request, 'classifyme/hasil.html', context)
