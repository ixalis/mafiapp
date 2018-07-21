from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^player/(?P<playername>\w+)/$', views.playerprofile, name='playerprofile'),
    url(r'^item/(?P<itemid>\w+)/$', views.itemprofile, name='itemprofile'),
    url(r'^ability/(?P<abilityid>\w+)/$', views.abilityprofile, name='abilityprofile'),
    url(r'^attribute/(?P<attributeid>\w+)/$', views.attributeprofile, name='attributeprofile'),
    url(r'^item/generate/(?P<itemid>\w+)/$', views.generateitem, name='generateitem'),
    url(r'^history/$', views.history, name='history'),
    url(r'^playerinbox/(?P<playername>\w+)/$', views.playerinbox, name='playerinbox'),
    url(r'^GMAbility/(?P<abilityname>\w+)$', views.GMAbility, name='GMAbility')

]
