from django.shortcuts import render
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
    if request.method == "POST":
        form = BukuForm(request.POST)
        if form.is_valid():
            buku = form.save(commit=False)
            buku.save()
            return redirect('textmining', id=buku_id)
    else:
        form = BukuForm()
    return render(request, 'classifyme/input.html', {'form': form})

def textmining(request):
    buku_id = request.POST['buku']
    selected_buku = Buku.objects.get(id=int(buku_id))
    return render(request, 'classifyme/textmining.html', {})
