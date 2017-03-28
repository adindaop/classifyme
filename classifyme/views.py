from django.shortcuts import render, get_object_or_404
from .forms import BukuForm
from .models import Buku
from django.shortcuts import redirect

def admin(request):
    return render(request, admin.site.urls, {})

def home(request):
    return render(request, 'classifyme/home.html', {})

def input(request):
    form = BukuForm()
    return render(request, 'classifyme/input.html', {'form': form})
