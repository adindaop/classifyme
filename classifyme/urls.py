from django.conf.urls import url
from . import views

urlpatterns = [
    #/admin/
    url(r'admin/$', views.admin, name='admin'),
    #/classifyme/
    url(r'^classifyme/$', views.home, name='home'),
    #/classifyme/input/
    url(r'^classifyme/input/$', views.input, name='input'),
    #/classifyme/input/1/
    url(r'^classifyme/input/(?P<buku_id>\d+)/$', views.textmining, name='textmining'),
    #/classifyme/input/1/klasifikasi
    url(r'^classifyme/input/(?P<buku_id>\d+)/klasifikasi/$', views.klasifikasi, name='klasifikasi'),
    #/classifyme/input/1/klasifikasi/hasil
    url(r'^classifyme/input/(?P<buku_id>\d+)/klasifikasi/hasil/$', views.hasil, name='hasil'),
]
