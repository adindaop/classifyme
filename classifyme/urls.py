from django.conf.urls import url
from . import views

urlpatterns = [
    #/admin/
    url(r'admin/$', views.admin, name='admin'),
    #/classifyme/
    url(r'^classifyme/$', views.home, name='home'),
    #/classifyme/input/
    url(r'^classifyme/input/$', views.input, name='input'),
]
