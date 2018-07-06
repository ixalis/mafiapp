from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    #url(r'^inv/$', views.inv.as_view(), name='inv'),
    #url(r'^(?P<playername>\w+)/$', views.inventory, name='inventory'),
    #url(r'^inventory$', views.inv.as_view(), name='inv')
]

