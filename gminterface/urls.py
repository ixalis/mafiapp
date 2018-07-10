from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^player/(?P<playername>\w+)/$', views.playerprofile, name='playerprofile'),
    url(r'^item/(?P<itemname>\w+)/$', views.itemprofile, name='itemprofile'),
    url(r'^ability/(?P<abilityname>\w+)/$', views.abilityprofile, name='abilityprofile'),
    url(r'^attribute/(?P<attributename>\w+)/$', views.attributeprofile, name='attributeprofile'),


]
