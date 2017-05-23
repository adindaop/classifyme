import csv
from django.shortcuts import render, get_object_or_404
from .forms import BukuForm
from .models import Buku
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
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

def edit_data(request, buku_id):
    buku = get_object_or_404(Buku, id=buku_id)
    if request.method == 'POST':
        form = BukuForm(request.POST, request.FILES, instance=buku)
        if form.is_valid():
            buku.save()
            return HttpResponseRedirect(reverse('classifyme:data',))
    else:
        form = BukuForm(instance=buku)
    return render(request, 'classifyme/edit.html', {'form': form})

def textmining(request, buku_id):
    buku = get_object_or_404(Buku, id=buku_id)
    context = {}
    selected_buku = Buku.objects.get(id=int(buku_id))
    context['buku'] = selected_buku

    #membuka file training set positif
    training_set_positif = ''
    with open('media/{}'.format(selected_buku.training_set_positif.file)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_positif = 0
        for row in csvreader:
            total_row_positif += 1
            training_set_positif += row['Review']
    context['total_row_positif'] = total_row_positif
    context['training_set_positif'] = training_set_positif

    #preprocessing
    filtered_word_positif = []
    stop_words = set(stopwords.words("bahasa"))
    word_list = set(stopwords.words("wordlist"))
    case_folding_pos = training_set_positif.lower() #case folding
    tokenized_words_positif = word_tokenize(case_folding_pos) #tokenizing
    for w in tokenized_words_positif:
        if w not in stop_words and w in word_list: #filtering
            filtered_word_positif.append(w)
    context['filtered_word_positif'] = filtered_word_positif

    #count(w, training_pos)
    word_counts = collections.Counter(filtered_word_positif)
    wordfreq_positif_list = []
    for w, cp in sorted(word_counts.items()):
        wordfreq_positif_list.append({'w': w, 'cp': cp})
    #print('WORDFREQ_POSITIF_LIST', wordfreq_positif_list)
    context['wordfreq_positif_list'] = wordfreq_positif_list

    #jumlah kata dalam training set positif
    jumlah_kata_positif = len(filtered_word_positif)
    print('JUMLAH_KATA_POSITIF', jumlah_kata_positif)
    context['jumlah_kata_positif'] = jumlah_kata_positif

    #membuka file training set negatif
    training_set_negatif = ''
    with open('media/{}'.format(selected_buku.training_set_negatif.file)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_negatif = 0
        for row in csvreader:
            total_row_negatif += 1
            training_set_negatif += row['Review']
    context['total_row_negatif'] = total_row_negatif
    context['training_set_negatif'] = training_set_negatif

    #preprocessing
    filtered_word_negatif = []
    stop_words = set(stopwords.words("bahasa"))
    word_list = set(stopwords.words("wordlist"))
    case_folding_neg = training_set_negatif.lower() #case folding
    tokenized_words_negatif = word_tokenize(case_folding_neg) #tokenizing
    for w in tokenized_words_negatif:
        if w not in stop_words and w in word_list: #filtering
            filtered_word_negatif.append(w)
    context['filtered_word_negatif'] = filtered_word_negatif

    #count(w, training_neg)
    word_counts = collections.Counter(filtered_word_negatif)
    wordfreq_negatif_list = []
    for w, cp in sorted(word_counts.items()):
        wordfreq_negatif_list.append({'w': w, 'cp': cp})
    context['wordfreq_negatif_list'] = wordfreq_negatif_list

    #jumlah kata dalam training set negatif
    jumlah_kata_negatif = len(filtered_word_negatif)
    print('JUMLAH_KATA_NEGATIF', jumlah_kata_negatif)
    context['jumlah_kata_negatif'] = jumlah_kata_negatif

    #total ulasan
    total_ulasan = total_row_positif + total_row_negatif
    context['total_ulasan'] = total_ulasan

    #priors positif
    priors_pos = float(total_row_positif / total_ulasan)
    context['priors_pos'] = priors_pos

    #priors negatif
    priors_neg = float(total_row_negatif / total_ulasan)
    context['priors_neg'] = priors_neg

    #menyimpan hasil priors ke django model field
    selected_priors = Buku.objects.get(id=int(buku_id))
    selected_priors.priors_pos = priors_pos
    selected_priors.priors_neg = priors_neg
    selected_priors.save()

    #kata unik
    unique_words = filtered_word_positif + filtered_word_negatif
    unique_wordfreq_total = nltk.FreqDist(unique_words)
    total_unique_words = unique_wordfreq_total.most_common()
    context['total_unique_words'] = total_unique_words

    #|V| / jumlah kata unik seluruh data percobaan
    unique_wordfreq_total = nltk.FreqDist(unique_words)
    wordfreq_sample_total = 0
    for sample in unique_wordfreq_total:
        wordfreq_sample_total += 1
    print('JUMLAH_KATA_UNIK', wordfreq_sample_total)
    context['wordfreq_sample_total'] = wordfreq_sample_total

    #membuka file testing set
    testing_set = ''
    with open('media/{}'.format(selected_buku.testing_set)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        total_row_testing = 0
        for row in csvreader:
            total_row_testing += 1
            testing_set += row['Review']
    print('total_row_testing', total_row_testing)
    context['testing_set'] = testing_set

    #preprocessing
    filtered_word_testing = []
    stop_words = set(stopwords.words("bahasa"))
    word_list = set(stopwords.words("wordlist"))
    case_folding_test = testing_set.lower() #case folding
    tokenized_words_testing = word_tokenize(case_folding_test) #tokenizing
    for w in tokenized_words_testing:
        if w not in stop_words and w in word_list: #filtering
            filtered_word_testing.append(w)
    print('FILTERED_WORD_TESTING', filtered_word_testing)
    context['filtered_word_testing'] = filtered_word_testing

    #count(w, testing)
    word_counts = collections.Counter(filtered_word_testing)
    wordfreq_testing_list = []
    for w, freq_test in sorted(word_counts.items()):
        if w in filtered_word_testing:
            wordfreq_testing_list.append({'w': w, 'freq_test': freq_test})
    print('WORDFREQ_TESTING_LIST', wordfreq_testing_list)
    context['wordfreq_testing_list'] = wordfreq_testing_list

    #count(w,positif) + 1
    wordfreq_test_in_pos = []
    for item_testing in wordfreq_testing_list:
        for item_positif in wordfreq_positif_list:
            if item_testing['w'] == item_positif['w']:
                cp = (item_positif['cp']+1)
                break
        else:
            cp = 1
        wordfreq_test_in_pos.append({'kata': item_testing['w'], 'cp': cp})
    print('WORDFREQ_TEST_IN_POS', wordfreq_test_in_pos)
    context['wordfreq_test_in_pos'] = wordfreq_test_in_pos

    #conditional probabilities positif
    cp_pos_list = []
    for item in wordfreq_test_in_pos:
        if item['kata'] not in cp_pos_list:
            pembilang = item['cp']
            penyebut = jumlah_kata_positif + wordfreq_sample_total
            hasil = float(pembilang/penyebut)
            cp_pos_list.append({'kata': item['kata'], 'hasil': hasil})
    print('CP_POS_LIST', cp_pos_list)
    context['cp_pos_list'] = cp_pos_list

    #hasil akhir positif
    product_cp_pos = 1
    cp_words_pos = []
    i = 0
    while i < len(cp_pos_list):
        cp_words_pos.append(cp_pos_list[i]['hasil'] ** wordfreq_testing_list[i]['freq_test']) #cp**jumlah_kata
        i += 1
    for x in cp_words_pos:
        product_cp_pos *=x #pengalian semua objek dalam list
    hasil_pos = selected_buku.priors_pos * product_cp_pos #pengalian hasil keseluruhan dengan priors
    print('HASIL_POS', hasil_pos)
    context['hasil_pos'] = hasil_pos

    #count(w,negatif) + 1
    wordfreq_test_in_neg = []
    for item_testing in wordfreq_testing_list:
        for item_negatif in wordfreq_negatif_list:
            if item_testing['w'] == item_negatif['w'] :
                cp = (item_negatif['cp']+1)
                break
        else:
            cp = 1
        wordfreq_test_in_neg.append({'kata': item_testing['w'], 'cp': cp})
    print('WORDFREQ_TEST_IN_NEG', wordfreq_test_in_neg)
    context['wordfreq_test_in_neg'] = wordfreq_test_in_neg

    #conditional probabilities negatif
    cp_neg_list = []
    for item in wordfreq_test_in_neg:
        if item['kata'] not in cp_neg_list:
            pembilang = item['cp']
            penyebut = jumlah_kata_negatif + wordfreq_sample_total
            hasil = float(pembilang/penyebut)
            cp_neg_list.append({'kata': item['kata'], 'hasil': hasil})
    print('CP_NEG_LIST', cp_neg_list)
    context['cp_neg_list'] = cp_neg_list

    #hasil akhir negatif
    product_cp_neg = 1
    cp_words_neg = []
    i = 0
    while i < len(cp_neg_list):
        cp_words_neg.append(cp_neg_list[i]['hasil'] ** wordfreq_testing_list[i]['freq_test']) #cp**jumlah_kata
        i += 1
    for x in cp_words_neg:
        product_cp_neg *=x #pengalian semua objek dalam list
    hasil_neg = selected_buku.priors_neg * product_cp_neg #pengalian hasil keseluruhan dengan priors
    print('HASIL_NEG', hasil_neg)
    context['hasil_neg'] = hasil_neg

    #menyimpan hasil akhir ke django model field
    selected_hasil = Buku.objects.get(id=int(buku_id))
    selected_hasil.hasil_pos = hasil_pos
    selected_hasil.hasil_neg = hasil_neg
    selected_hasil.save()

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
        hasil_akhir = "Data Overload"
    context['hasil_akhir'] = hasil_akhir

    #menyimpan hasil klasifikasi ke django model field
    selected_hasil = Buku.objects.get(id=int(buku_id))
    selected_hasil.hasil_klasifikasi = hasil_akhir
    selected_hasil.save()

    return render(request, 'classifyme/hasil.html', context)
