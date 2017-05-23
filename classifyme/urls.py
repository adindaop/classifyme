from django.conf.urls import url
from . import views

urlpatterns = [
    #/admin/
    url(r'admin/$', views.admin, name='admin'),
    #/classifyme/
    url(r'^classifyme/$', views.home, name='home'),
    #/classifyme/input/
    url(r'^classifyme/input/$', views.input, name='input'),
    #/classifyme/input/data/
    url(r'^classifyme/input/data/$', views.data, name='data'),
    #popup
    url(r'^classifyme/input/data(?P<buku_id>\d+)/$', views.edit_data, name='edit_data'),
    #/classifyme/input/data/1/
    url(r'^classifyme/input/data/(?P<buku_id>\d+)/$', views.textmining, name='textmining'),
    #/classifyme/input/data/1/hasil
    url(r'^classifyme/input/data/(?P<buku_id>\d+)/hasil/$', views.hasil, name='hasil'),
]
