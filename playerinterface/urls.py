from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^item/(?P<itemid>\w+)/$', views.iteminstance, name='iteminstance'),
    url(r'^item/use/(?P<itemid>\w+)/$', views.itemuse, name='itemuse'),
    url(r'^ability/(?P<abilityid>\w+)/$', views.abilityinstance, name='abilityinstance'),
    url(r'^ability/activate/(?P<abilityid>\w+)/$', views.abilityactivate, name='abilityactivate'),
]

